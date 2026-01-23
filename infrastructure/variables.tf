variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "eu-west-2" # London region, close to Isle of Wight
}

variable "bucket_name" {
  description = "Name of the S3 bucket for website hosting (must be globally unique)"
  type        = string
  default     = "two-lights-one-wight-website"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "cloudfront_price_class" {
  description = "CloudFront price class"
  type        = string
  default     = "PriceClass_100" # US, Canada, Europe
}
