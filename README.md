# Meilisearch on AWS with Terraform and GitHub Actions

This repository contains the necessary infrastructure as code (IaC) and CI/CD pipelines to deploy a Meilisearch instance on AWS. It uses Terraform to manage the infrastructure and GitHub Actions to automate the deployment process.

## How it Works

1.  **Push to `main`**: When you push code to the `main` branch of your GitHub repository, the `deploy.yml` workflow will automatically trigger.
2.  **Infrastructure Provisioning**: The workflow uses Terraform to create or update the AWS resources defined in the `terraform` directory. This includes an EC2 instance, an EBS volume for data persistence, and a security group.
3.  **Meilisearch Setup**: The workflow then SSHs into the EC2 instance and runs a script to install Docker, mount the EBS volume, and start the Meilisearch container.
4.  **Persistent Data**: The EBS volume is used to store the Meilisearch data, so your data will persist even if the EC2 instance is replaced. The deployment script includes a check to prevent the EBS volume from being reformatted on every deployment, ensuring your data is safe.

## Repository Structure

-   `/.github/workflows/deploy.yml`: The GitHub Actions workflow that automates deploying your Meilisearch instance to AWS.
-   `/app/main.py`: A sample Python application showing how to save and search for events in your Meilisearch instance.
-   `/app/requirements.txt`: The dependencies for the Python application.
-   `/terraform/main.tf`: The Terraform configuration for your AWS infrastructure (EC2, EBS, Security Group).
-   `/terraform/variables.tf`: Variables for your Terraform configuration. You can customize your AWS region, instance type, and EBS volume size here.
-   `/terraform/outputs.tf`: Terraform outputs, which includes the public IP of your EC2 instance.
-   `/.gitignore`: A standard gitignore file for Python and Terraform projects.

## Getting Started

To get this project up and running, follow these steps:

### 1. Create a GitHub Repository

Create a new repository on GitHub and push the code from this project.

### 2. AWS Prerequisites

-   Ensure you have an AWS account with the necessary permissions to create EC2 instances, EBS volumes, and security groups.
-   Create an EC2 key pair in the AWS console. You will need the name of this key pair for the GitHub secrets.
-   **Create an S3 Bucket**: Create a private S3 bucket with versioning enabled to store the Terraform state file (`terraform.tfstate`).
-   **Create a DynamoDB Table**: Create a DynamoDB table with a primary key named `LockID` (String type). This is for Terraform state locking.

### 3. Configure `backend.tf`

Update the `terraform/backend.tf` file with the names of the S3 bucket and DynamoDB table you just created.

### 4. Create an IAM Policy

The AWS user/role that your credentials belong to needs specific permissions for Terraform to manage the infrastructure and the remote state.

Create a new IAM policy with the JSON below and attach it to the IAM user or role you are using for deployment.

**Important:** Replace `YOUR_BUCKET_NAME`, `YOUR_DYNAMODB_TABLE_NAME`, and `YOUR_AWS_ACCOUNT_ID` with your actual resource names and account ID.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "TerraformS3Backend",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/meilisearch/terraform.tfstate"
        },
        {
            "Sid": "TerraformS3List",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME"
        },
        {
            "Sid": "TerraformDynamoDBLock",
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:DeleteItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:YOUR_AWS_ACCOUNT_ID:table/YOUR_DYNAMODB_TABLE_NAME"
        },
        {
            "Sid": "TerraformEC2",
            "Effect": "Allow",
            "Action": "ec2:*",
            "Resource": "*"
        }
    ]
}
```