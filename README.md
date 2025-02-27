# CS643 - Programming Assignment 2
## Machine Learning Model for Predicting Wine Quality

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

<img width="772" alt="Screenshot 2024-05-01 at 10 36 41 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/79c9ec98-e013-4f19-b04a-6e6278396570">

<img width="785" alt="Screenshot 2024-05-01 at 10 36 49 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/5236d37d-d606-4d5f-be33-458ba02f5f67">

<img width="775" alt="Screenshot 2024-05-01 at 10 36 58 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/eea4fee4-ffc2-48b4-a40d-28bdbe3735be">

<img width="757" alt="Screenshot 2024-05-01 at 10 37 25 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/1fb4e9e1-0c92-4eb4-8ccf-9e83c49d4c80">

<img width="766" alt="Screenshot 2024-05-01 at 10 37 32 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/aebeb909-14c4-412b-8210-25bf88397c79">

<img width="398" alt="Screenshot 2024-05-01 at 10 36 04 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/023be01d-6414-478c-854a-10a11786e5ae">

#### EC2 Configuration
- **Instance Selection**: Choose the Master EC2 instance from your cluster setup.
- **Security**: Update the security group to allow SSH access from your specific IP.
  <img width="1224" alt="Screenshot 2024-05-01 at 10 39 10 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/6b05fc0b-1f9f-47f2-8f57-3e7cb7182941">

- **Access**: Connect to the Master EC2 instance using SSH via PowerShell, authenticated with your EC2 Key pair.
  <img width="884" alt="Screenshot 2024-05-01 at 10 41 56 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/d13f7cf5-d870-4ba3-be7a-3f631f34fa2d">

- **AWS Setup**: Configure AWS Credentials and Session Token, and run initial setup commands:
  `aws s3api get-object --bucket sp3244wineapplication --key initialize.sh /home/hadoop/initialize.sh`
  `export acccess=<your-access-key>`
  `export secret=<your-secret-key>`
  `initialize init.sh`

  <img width="1056" alt="Screenshot 2024-05-01 at 10 44 39 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/8ea2c98f-7d53-4062-9eca-e673c85944c0">



### Code Execution
Run the training and prediction processes using the following commands:
```bash
spark-submit WineQualityTrainingAndPrediction.py train
```

```bash
python wine_quality_prediction.py predict
```
### Docker Implementation
- Create the Dockerfile
- Create a Docker Repository
- Build the Docker Image:
  `docker build -t winequality .`
  <img width="587" alt="Screenshot 2024-05-01 at 10 52 56 AM" src="https://github.com/Shiva-prakash-perumal/Aws_EMR_EC2_Wine_Quality_Prediction/assets/36128062/4d0561f7-2206-4407-9862-387b58d54829">

- Tag the Docker Image:
  `docker tag winequality sp3244/winequality:latest `
- Push the Docker Image to Docker Hub: `docker push sp3244/winequality:latest`

### Docker Execution

- Pull the Docker Image: `docker pull sp3244/winequality`
- Run the Docker Image: `docker run -v /Users/avi/Desktop/study/Aws_EMR_EC2_Wine_Quality_Prediction/ValidationDataset.csv:/app/ValidationDataset.csv  -ti sp3244/winequality:latest ValidationDataset.csv --predict`

  
