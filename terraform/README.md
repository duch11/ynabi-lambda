# Terraform

This terraform definition does the following:
- Creates an AWS lambda function for running ynabi (if you've put the code into the zip file)
- Creates an AWS log group which the lambda outputs it's logs to.
- Creates an AWS Eventbridge (Cloudwatch) Rule for triggering the lambda every 3 hours

**ONLY do this if you are comfortable with using AWS and Terraform.**

## Pre-requisites
- Have a `new_user_credentials.csv` file with credentials for an admin account on AWS.
- awscli v2
- Terraform >= v1.1.9 

See: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey


## Setup your environment

### WSL / Linux / OSX
```bash
aws configure import --csv file:///home/MY_USER/new_user_credentials.csv

# add to your bashrc:
export AWS_PROFILE="your-aws-profile-name"
```

### Windows
```powershell
aws configure import --csv file://C:\Users\MY_USER\new_user_credentials.csv

#Start > "Edit the system environment variables" > New > "Variable Name": AWS_PROFILE and "Variable value": "your-aws-profile-name"
```

## Deploy Infrastructure in AWS
1. Configure credentials and YNAB accounts etc
2. Run `python3 generate_lambda_zip.py` which will generate the zip file for terraform**
3. Use terraform to deploy as below: 

```
cd terraform/
terraform init
terraform plan
terraform apply
```

## Destroy Infrastructure in AWS
```
terraform destroy
```
