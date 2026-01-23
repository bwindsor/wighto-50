# GitHub Actions Deployment Guide

This document explains how to set up automated deployments for the "Two Lights, One Wight" website using GitHub Actions.

## Overview

The project includes a single GitHub Actions workflow:

**Deploy to AWS** (`deploy.yml`) - Automatically builds and deploys to AWS on push to main branch

## Setup Instructions

### 1. Required GitHub Secrets

Add the following secrets to your GitHub repository:

**Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description  | How to Get |
|------------|--------------|------------|
| `AWS_ROLE_ARN` | AWS Role ARN | Create in AWS IAM Console |

### 2. Create AWS IAM User

Create an IAM user with the following permissions:
