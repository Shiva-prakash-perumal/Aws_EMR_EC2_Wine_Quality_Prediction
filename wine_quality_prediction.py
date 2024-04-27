import sys
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
import boto3

s3Client = boto3.client('s3')

def GetDataFromS3(buc_name, fileKey):
    s3Client.get_object(buc_name, fileKey)

def UploadModelToS3(buc_name, localModelPath, s3ModelKey):
    s3Client.upload_file(localModelPath, buc_name, s3ModelKey)

def GrabColNames(df, catth=10, carth=20):
    catcols, numbutcat, cat_but_car = [], [], []
    for field in df.schema.fields:
        if str(field.dataType) == 'StringType':
            if df.select(field.name).distinct().count() > carth:
                cat_but_car.append(field.name)
            else:
                catcols.append(field.name)
        else:
            if df.select(field.name).distinct().count() < catth:
                numbutcat.append(field.name)

    catcols = list(set(catcols + numbutcat) - set(cat_but_car))
    num_cols = [field.name for field in df.schema.fields if str(field.dataType) != 'StringType' and field.name not in numbutcat]

    print(f"Observations: {df.count()}, Variables: {len(df.columns)}")
    print(f'cat_cols: {len(cat_cols)}, num_cols: {len(num_cols)}, cat_but_car: {len(cat_but_car)}, numbutcat: {len(numbutcat)}')
    return cat_cols, num_cols, cat_but_car

def get_models(labelCol):
    lr = LogisticRegression(featuresCol="scaledFeatures", labelCol=labelCol)

    return ("LR", lr, ParamGridBuilder()
             .addGrid(lr.maxIter, [10, 20, 50])
             .addGrid(lr.regParam, [0.01, 0.1, 0.5])
             .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0])
             .build())


def evaluate_models(training_data, validation_data, featuresCol, labelCol):
    featureIndexer = VectorAssembler(inputCols=featuresCol, outputCol="features")
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
    best_f1_score, best_cv_model, best_model_name = 0, None, ""
    evaluator = MulticlassClassificationEvaluator(labelCol=labelCol, predictionCol="prediction", metricName="f1")

    for name, model, paramGrid in get_models(labelCol):
        pipeline = Pipeline(stages=[featureIndexer, scaler, model])
        cv = CrossValidator(estimator=pipeline,
                            estimatorParamMaps=paramGrid,
                            evaluator=evaluator,
                            numFolds=5)
        cv_model = cv.fit(training_data)
        predictions = cv_model.transform(validation_data)
        f1_score = evaluator.evaluate(predictions)

        print(f"{name} - Best F1 Score: {f1_score:.2f}")

        if f1_score > best_f1_score:
            best_f1_score = f1_score
            best_model_name = name
            best_cv_model = cv_model.bestModel

    if best_cv_model:
        print(f"Best Model: {best_model_name} with F1 Score: {best_f1_score:.2f}")

    return best_cv_model

def predict_new_data(new_data_path):
    spark = SparkSession.builder.appName("Prediction Using Best Model").getOrCreate()
    new_data = spark.read.csv(GetDataFromS3(new_data_s3_path, "Test"), header=True, inferSchema=True)
    temp_quality_column_data = new_data.select("quality")
    new_data = new_data.drop("quality")
    best_model = PipelineModel.load("s3a://winequalityapplication/best_model")
    predictions = best_model.transform(new_data)
    predictions.select("prediction").show()
    predictions_with_column = predictions.join(temp_quality_column_data)
    evaluator = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction", metricName="f1")
    f1Score = evaluator.evaluate(predictions_with_column)
    print("f1Score ",f1Score)
    evaluator = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions_with_column)
    print("accuracy ",accuracy)
    spark.stop()

if __name__ == "__main__":

    spark = SparkSession.builder.appName("Model Training and Validation").getOrCreate()
    training_data_s3_path, validation_data_s3_path, new_data_s3_path, model_bucket = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    training_data = spark.read.csv(GetDataFromS3(training_data_s3_path, "Cleaned_TrainingData.csv"), header=True, inferSchema=True)
    validation_data = spark.read.csv(GetDataFromS3(validation_data_s3_path, "Cleaned_ValidationData.csv"), header=True, inferSchema=True)

    cat_cols, num_cols, cat_but_car = GrabColNames(training_data)
    featuresCol = cat_cols + num_cols
    featuresCol = [col for col in featuresCol if col != 'quality']
    labelCol = 'quality'

    if '--train' in sys.argv:
        best_model = evaluate_models(training_data, validation_data, featuresCol, labelCol)
        local_model_path = '/best_model'
        best_model.write().overwrite().save(local_model_path)
        UploadModelToS3(model_bucket, local_model_path, 'best_model')

    if '--predict' in sys.argv:
        predict_new_data(new_data_s3_path)

    spark.stop()