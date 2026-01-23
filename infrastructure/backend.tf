# Terraform Backend Configuration
# Store state in S3 with DynamoDB locking
#

terraform {
  backend "s3" {
    # Update this with your actual state bucket name from bootstrap
    bucket = "two-lights-one-wight-tfstate"

    key            = "two-lights-one-wight/terraform.tfstate"
    region         = "eu-west-2"

    # Enable encryption at rest
    encrypt = true

    # Optional: Use versioning for state history
    # versioning = true
  }
}
