# YNABI-Lambda: Spiir to YNAB import script for use on AWS Lambda.

Since YNAB does not support Nordic banks, the original author created this Python script
to import Spiir transactions into YNAB. The script is not endorsed by Spiir
or YNAB and may stop working at any time.

## Getting started

### Spiir: Setup Credentials (REQUIRED)

Add your Spiir login credentials to ynabi/api/credentials.py
(see ynabi/api/credentials.example.py).

### YNAB: Setup API token (REQUIRED)

- Add your API token to `./ynabi/api/credentials.py`

(Get your YNAB Personal Access Token by following the instructions:
https://api.youneedabudget.com/#personal-access-tokens.)

### YNAB: Setup Budget ID (REQUIRED)

- Get in the url to your budget: ie. `https://app.youneedabudget.com/YOUR-BUDGET-ID-IS-HERE/budget`
- Add your budget-ID to `ynabi/api/credentials.py`.

### YNAB: Rename Account Names in to Match SPIIR (REQUIRED)

*IMPORTANT: BE EXACT, OR IT WONT WORK*

- Rename your accounts in YNAB to what they're named in Spiir.

## Requirements

- Python 3.8 or above

## Installation

0. Clone this repo.
1. Do the required configuration above
2. `py -m venv venv`
3. `pip install requests`

## Run it:

Two options, locally or on AWS.

*Warning: AWS/cloud setup, requires an AWS account and basic knowledge about Amazon Web Services.* 


### Locally

Have python installed (min version 3.8)

`py ./lambda_function.py`


### On AWS Lambda

*Warning: AWS/cloud setup, requires an AWS account and basic knowledge about Amazon Web Services.* 

0. Do the "Configure the basics" steps
1. Copy `./ynabi/` into ./extras/aws_lambda_code.zip (this zip file contains the requests library for use in AWS Lambda)
2. Copy `lambda_function.py` into ./extras/aws_lambda_code.zip
3. Upload to the AWS lambda service 
4. Setup an amazon event bridge to trigger it daily

### In case of issues:

See AWS documentation: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

