import sys
import os
import boto3
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, FloatType
from pyspark.ml import PipelineModel, Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

access = os.getenv("access")
secret = os.getenv("secret")

s3_client = boto3.client('s3')

def get_s3_data(buc, s3_directory, folder):
    s3_data = boto3.client('s3')
    paginat = s3_data.get_paginator('list_objects_v2')
    for x in paginat.paginate(Bucket=buc, Prefix=s3_directory):
        for object in x.get('Contents', []):
            filepath = os.path.join(folder, object['Key'][len(s3_directory):])
            directory = os.path.dirname(filepath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            s3_data.download_file(buc, obj['Key'], filepath)

def GetColumnNames(df, CAT=10, CHAR=20):
    CAT_columns, n, c = [], [], []
    for f in df.schema.fields:
        count = df.select(f.name).distinct().count()
        if str(f.dataType) == 'StringType':
            if count > CHAR:
                c.append(f.name)
            else:
                CAT_columns.append(f.name)
        elif count < CAT:
            n.append(f.name)

    CAT_columns = list(set(CAT_columns) - set(c))
    cols = [f.name for f in df.schema.f if str(f.dataType) != 'StringType' and f.name not in n]
    return CAT_columns, cols, c

def transformed_df(df):
    cols = ["fixed acidity", "volatile acidity", "citric acid", "residual sugar",
            "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density",
            "pH", "sulphates", "alcohol"]
    for c in cols:
        df = df.withColumn(c, df[c].cast(FloatType()))
    df = df.withColumn('quality', df['quality'].cast(IntegerType()))
    return df

def get_df_from_s3(k, s, transformed_df):
    Resp = s3_client.get_object(Bucket='sp3244wineapplication', Key=k)
    d_string = Resp['Body'].read().decode('utf-8').replace('"', '')
    d_list = [tuple(x.split(';')) for x in d_string.strip().split('\r\n') if x]
    col = list(d_list.pop(0))
    df = s.createDataFrame(d_list, col)
    return transformed_df(df)

def get_LR_params(Col_Label):
    LogicR = LogisticRegression(featuresCol="scaledFeatures", labelCol=Col_Label)

    return [
        ("LogicR", LogicR, ParamGridBuilder()
             .addGrid(LogicR.maxIter, [10, 20, 50])
             .addGrid(LogicR.regParam, [0.01, 0.1, 0.5])
             .addGrid(LogicR.elasticNetParam, [0.0, 0.5, 1.0])
             .build())
    ]

def Model_evaluation(t_data, v_data, f_Col, Col_Label):
    Assemblers = VectorAssembler(inputCols=f_Col, outputCol="features")
    Scal = StandardScaler(inputCol="features", outputCol="scaledFeatures")
    Eval = MulticlassClassificationEvaluator(labelCol=Col_Label, metricName="f1")
    F1score, Finalmodel = 0, None

    for n, m, p in get_LR_params(Col_Label):
        pipeline = Pipeline(stages=[Assemblers, Scal, m])
        cross_V = CrossValidator(estimator=pipeline, estimatorParamMaps=p, evaluator=Eval, numFolds=5)
        cross_V_model = cross_V.fit(t_data)
        F1 = Eval.evaluate(cross_V_model.transform(v_data))
        if F1 > F1score:
            F1score, Finalmodel = F1, cross_V_model.bestModel
            print(f"{n} - F1 Score: {F1:.3f}")

    return Finalmodel

def prediction(path, s, Finalmodel):
    df_new = get_df_from_s3(path, s, transformed_df)
    temp_column = df_new.select("quality")
    df_new = df_new.drop("quality")
    predict = Finalmodel.transform(df_new)
    predict.show()
    predict_cols = predict.join(temp_column)
    Eval = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction", metricName="f1")
    F1 = Eval.evaluate(predict_cols)
    print(f"F1 Score is  {F1:.3f}")
    Eval = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction", metricName="accuracy")
    acc = Eval.evaluate(predict_cols)
    print(f"accuracy is {acc:.3f}")

if __name__ == "__main__":
    s = SparkSession.builder.appName("Prediction of wine Quality") \
        .config("spark.jars", "hadoop-aws-3.0.0.jar,aws-java-sdk-1.11.375.jar") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem").getOrCreate()

    s._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    s._jsc.hadoopConfiguration().set("fs.s3a.access.key", f"{access}")
    s._jsc.hadoopConfiguration().set("fs.s3a.secret.key", f"{secret}")
    t_df = get_df_from_s3('TrainingDataset.csv', s, transformed_df)
    v_df = get_df_from_s3('ValidationDataset.csv', s, transformed_df)
    CAT_columns, cols, _ = GetColumnNames(t_df)

    f_Col = CAT_columns + cols
    if 'quality' in f_Col:
        f_Col.remove('quality')

    if 'train' in sys.argv:
        Finalmodel = Model_evaluation(t_df, v_df, f_Col, 'quality')
        model_dir = "s3://sp3244wineapplication/bestmodel"
        Finalmodel.write().overwrite().save(model_dir)

    if 'predict' in sys.argv:
        get_s3_data('sp3244wineapplication','bestmodel/','/home/hadoop/bestmodel')
        Finalmodel = PipelineModel.load('/home/hadoop/bestmodel')
        prediction('TestDataset.csv', s, Finalmodel)

    s.stop()