FROM amazonlinux:latest

RUN yum install -y java-1.8.0-openjdk-devel && \
    yum clean all

ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk

WORKDIR /app

COPY WineQualityTrainingAndPrediction.py /app/
COPY CleanTrainingDataset.csv /app/
COPY CleanValidationDataset.csv /app/
COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

RUN yum update -y && \
    yum install -y python36 python36-pip && \
    yum clean all

ENTRYPOINT ["/app/entrypoint.sh"]

