# Use amazonlinux as the base image
FROM amazonlinux:latest

# Install OpenJDK 8
RUN yum install -y java-1.8.0-openjdk-devel && \
    yum clean all

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk

# Set the working directory
WORKDIR /app

# Copy your Python script and datasets into the Docker image
COPY WineQualityTrainingAndPrediction.py /app/
COPY CleanTrainingDataset.csv /app/
COPY CleanValidationDataset.csv /app/
COPY entrypoint.sh /app/

# Make sure your entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Update yum and install Python and pip
RUN yum update -y && \
    yum install -y python36 python36-pip && \
    yum clean all

# Set the entrypoint to run your application
ENTRYPOINT ["/app/entrypoint.sh"]

