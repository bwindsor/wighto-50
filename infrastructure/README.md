# Two Lights, One Wight - Infrastructure

This directory contains Terraform configuration to deploy the "Two Lights, One Wight" website to AWS using S3 and CloudFront.

## Architecture

- **S3 Bucket**: Hosts the static website files from the `dist` folder
- **CloudFront**: CDN distribution with HTTPS (redirects HTTP to HTTPS)
- **Origin Access Control (OAC)**: Ensures S3 bucket is only accessible via CloudFront
- **Security**: S3 bucket is private with no direct public access

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **Terraform** installed (version >= 1.0)
4. **Built website**: Run `npm run build` in the project root to create the `dist` folder

## Setup Instructions

### 1. Configure AWS Credentials
