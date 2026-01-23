#!/bin/bash
# Deployment script for Two Lights, One Wight website

set -e

echo "================================================"
echo "Two Lights, One Wight - Website Deployment"
echo "================================================"
echo ""

# Check if we're in the infrastructure directory
if [ ! -f "main.tf" ]; then
    echo "Error: This script must be run from the infrastructure directory"
    exit 1
fi

# Check if Terraform is initialized
if [ ! -d ".terraform" ]; then
    echo "Initializing Terraform..."
    terraform init
    echo ""
fi

# Build the website
echo "Step 1: Building website..."
cd ..
npm run build

if [ ! -d "dist" ]; then
    echo "Error: dist folder not found after build"
    exit 1
fi

cd infrastructure

# Get bucket name and distribution ID
echo ""
echo "Step 2: Getting AWS resource details..."
BUCKET_NAME=$(terraform output -raw s3_bucket_name 2>/dev/null || echo "")
DISTRIBUTION_ID=$(terraform output -raw cloudfront_distribution_id 2>/dev/null || echo "")

if [ -z "$BUCKET_NAME" ]; then
    echo "Error: Could not get S3 bucket name. Has Terraform been applied?"
    echo "Run 'terraform apply' first to create the infrastructure."
    exit 1
fi

# Sync files to S3
echo ""
echo "Step 3: Uploading files to S3..."
aws s3 sync ../dist/ s3://${BUCKET_NAME}/ \
    --delete \
    --cache-control "public,max-age=3600" \
    --exclude "*.html" \
    --exclude "*.json"

# Upload HTML files with shorter cache
aws s3 sync ../dist/ s3://${BUCKET_NAME}/ \
    --cache-control "public,max-age=300" \
    --exclude "*" \
    --include "*.html" \
    --include "*.json"

echo "Files uploaded successfully!"

# Invalidate CloudFront cache
echo ""
echo "Step 4: Invalidating CloudFront cache..."
INVALIDATION_ID=$(aws cloudfront create-invalidation \
    --distribution-id ${DISTRIBUTION_ID} \
    --paths "/*" \
    --query 'Invalidation.Id' \
    --output text)

echo "CloudFront invalidation created: ${INVALIDATION_ID}"

# Display website URL
echo ""
echo "================================================"
echo "✅ Deployment Complete!"
echo "================================================"
echo ""
echo "Website URL:"
terraform output website_endpoint
echo ""
echo "Note: CloudFront cache invalidation may take a few minutes to complete."
echo "Your changes should be visible shortly."
echo ""
