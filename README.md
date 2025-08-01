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

### 3. Configure GitHub Secrets

You need to add the following secrets to your GitHub repository's settings (`Settings > Secrets and variables > Actions > New repository secret`):

-   `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
-   `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
-   `AWS_KEY_NAME`: The name of the EC2 key pair you created in the previous step.
-   `AWS_PRIVATE_KEY`: The private key portion of the EC2 key pair you created.
-   `MEILI_MASTER_KEY`: A secure master key for your Meilisearch instance. You should generate a strong random string for this.

### 4. Deploy

Push your changes to the `main` branch. The GitHub Actions workflow will automatically run and deploy your Meilisearch instance.

### 5. Access Meilisearch

After the deployment is complete, you can find the public IP address of your EC2 instance in the output of the GitHub Actions workflow. You can also get it by running `terraform -chdir=terraform output meilisearch_public_ip` locally (assuming you have Terraform and your AWS credentials configured).

You can then use the Python application in the `app` directory to interact with your Meilisearch instance by setting the following environment variables:

```bash
export MEILI_URL="http://<your-ec2-instance-ip>:7700"
export MEILI_MASTER_KEY="<your-meili-master-key>"
```

Then run the application:

```bash
pip install -r app/requirements.txt
python app/main.py
```
