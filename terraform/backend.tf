terraform {
  backend "s3" {
    bucket         = "adgfe" # IMPORTANT: Replace with your S3 bucket name
    key            = "meilisearch/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "terraform-lock" # IMPORTANT: Replace with your DynamoDB table name
  }
} 