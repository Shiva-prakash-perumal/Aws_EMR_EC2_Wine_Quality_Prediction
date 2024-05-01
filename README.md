# CS643 - Programming Assignment 2
## Machine Learning Model for Predicting Wine Quality

### UCID: sp3244 
### Name: Shiva Prakash Perumal

### Project Overview
The goal of this project is to develop a Python program that makes use of the PySpark interface. An Elastic MapReduce (EMR) cluster from Amazon Web Services (AWS) hosts the application. Its primary objective is to use publicly available data to train a machine learning model in parallel on EC2 instances to predict wine quality. The model is used to forecast wine quality after training. The trained machine learning model's container image is created using Docker, which streamlines the deployment procedure.

### Main Python Script
**wine_quility_prediction.py:**:
  if given ‘train’ as a parameter, it Trains the model in parallel on an EMR Spark cluster by reading the training dataset from S3. After training, the model can be run via S3 on test data that has been supplied. The trained model is kept in the S3 bucket by the program.
  If given ‘--predict’ we use a pre-existing test data file to run the trained model. As a measure of the trained model's correctness, this application prints the F1 score.


### Repository Links
- [Docker Repository](https://hub.docker.com/repository/docker/sp3244/winequality/general)

### AWS Configuration

#### Amazon S3
- **Setup**: Create a bucket and upload the training and validation datasets, along with the `WineQualityTrainingAndPrediction.py` script.
- **Model Storage**: Create a `model` folder within the bucket to store the best performing model from training.

#### Amazon EMR
<img width="1512" alt="Screenshot 2024-05-01 at 10 35 56 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/fb36eaf9-45c6-460f-9610-b10e0c464c61">

#### EC2 Configuration
- **Instance Selection**: Choose the Master EC2 instance from your cluster setup.
- **Security**: Update the security group to allow SSH access from your specific IP.
- **Access**: Connect to the Master EC2 instance using SSH via PowerShell, authenticated with your EC2 Key pair.
- **AWS Setup**: Configure AWS Credentials and Session Token, and run initial setup commands:
  `aws s3api get-object --bucket sp3244wineapplication --key initialize.sh /home/hadoop/initialize.sh`
  `export acccess=<your-access-key>`
  `export secret=<your-secret-key>`
  `initialize init.sh`


### Code Execution
Run the training and prediction processes using the following commands:
```bash
spark-submit WineQualityTrainingAndPrediction.py --train
```


```bash
spark-submit WineQualityTrainingAndPrediction.py --predict
```
### Docker Implementation
- Create the Dockerfile
- Create a Docker Repository
- Build the Docker Image:
  `docker build -t winequality .`
- Tag the Docker Image:
  `docker tag winequality sp3244/winequality:latest `
- Push the Docker Image to Docker Hub: `docker push sp3244/winequality:latest`

### Docker Execution

- Pull the Docker Image: `docker pull sp3244/winequality`
- Run the Docker Image: `docker run -v /Users/avi/Desktop/study/Aws_EMR_EC2_Wine_Quality_Prediction/ValidationDataset.csv:/app/ValidationDataset.csv  -ti sp3244/winequality:latest ValidationDataset.csv --predict`

  
