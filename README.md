# CS643 - Programming Assignment 2
## Wine Quality Prediction ML Model

This project develops a Python application leveraging the PySpark interface on an AWS Elastic MapReduce (EMR) cluster. The goal is to train a machine learning model on EC2 instances to predict wine quality using public datasets. Docker is utilized to deploy a containerized version of the model.

### Primary Python Source File

- `WineQualityTrainingAndPrediction.py`: This script reads the training dataset from S3, trains the model using Logistic Regression and Decision Tree Classifier on an EMR Spark cluster, and selects the model with the best F1 score. It then executes predictions on test data stored in S3, printing the F1 score to assess accuracy.

### Repository Links

- [GitHub Repository](https://github.com/sky09998/WineQualityApplication)
- [Docker Hub Repository](https://hub.docker.com/repository/docker/sky09998/winequalityapplication/)

### AWS Configuration

#### Amazon S3
- Create a bucket and upload the training and validation datasets.
- Upload `WineQualityTrainingAndPrediction.py`.
- Create a folder named `model` to store the best model from training.

#### Amazon EMR
Images here

#### EC2 Configuration
- Choose the Master EC2 instance from your cluster setup.
- Add an inbound rule to the security group for SSH access from your specified custom IP.
- Log in to the Master EC2 instance using PowerShell, utilizing the Public DNS with the SSH command authenticated by the previously created EC2 Key pair.
- Configure AWS Credentials and AWS Session Token.
- Run initial setup commands:
  `aws s3api get-object --bucket winequalityapplication --key init.sh /home/hadoop/init.sh`

  `export AWS_ACCESS_KEY_ID=<your-access-key>`

  `export AWS_SECRET_ACCESS_KEY=<your-secret-key>`

  `sh init.sh`


### Code Implementation

```bash
spark-submit WineQualityTrainingAndPrediction.py --train
```
```bash
spark-submit WineQualityTrainingAndPrediction.py --predict
```
## Docker Implementation

### Steps to Create and Manage Docker Images

1. **Create the Dockerfile**
   - Prepare the Dockerfile with the required configurations and dependencies.

2. **Create a Docker Repository**
   - Navigate to your Docker profile and create a repository named `mlapplication_pa2`.

3. **Build the Docker Image**
   - Run the following command to build your Docker image:
     ```
     docker build -t mlapplication .
     ```

4. **Tag the Docker Image**
   - After building the image, tag it for pushing to Docker Hub:
     ```
     docker tag mlapplication username/mlapplication_pa2
     ```

5. **Push the Docker Image to Docker Hub**
   - Push the tagged image to your Docker Hub repository:
     ```
     docker push username/mlapplication_pa2
     ```

6. **Pull the Docker Image**
   - When you need to pull the image from Docker Hub, use:
     ```
     docker pull username/mlapplication_pa2
     ```