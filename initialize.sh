#!/bin/bash
pip install pyspark
pip install numpy
pip install boto3
aws s3api get-object --bucket sp3244wineapplication --key wine_quality_prediction.py /home/hadoop/wine_quality_prediction.py
curl -o hadoop-aws-3.0.0.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.0.0/hadoop-aws-3.0.0.jar
curl -o aws-java-sdk-1.11.375.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.375/aws-java-sdk-1.11.375.jar