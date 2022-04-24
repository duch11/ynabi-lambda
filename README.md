# YNABI-Lambda - Make Spiir ❤️ YNAB
Spiir-to-YNAB import script. 

Get a taste of auto-sync for YNAB through Spiir & Nordic API Gateway 💵 😎

### 🛠️This Python script automates what you already could do yourself manually:
1. It Downloads your transactions from Spiir 💚 
2. It Converts the transaction format a bit 🛑->✅ 
3. Then it Imports them into YNAB 💙📅🙍💵📊

🧡☁️ Now with AWS Lambda Cloud support! ☁️🧡

**The script is not endorsed by Spiir or YNAB and may stop working at any time.**

<p style="text-align:center;"><img src="extras\ynabi-lambda-logo.png"  width="800" /></p>

## 🛠️ Getting started - Configuring `credentials.py` 🛠️
Add the following to your `./ynabi/api/credentials.py` file

### Add your Spiir login credentials

- Credentials: Your username and password you would use for: www.mine.spiir.dk/log-ind

### Add your YNAB API token

- Follow the instructions: https://api.youneedabudget.com/#personal-access-tokens - to get your YNAB Personal Access Token.

### Add your budget-ID to `ynabi/api/credentials.py`

Get the ID from the url for your budget:
Example: `https://app.youneedabudget.com/YOUR-BUDGET-ID-IS-HERE/budget`

## Rename Account Names in YNAB so they Match Spiir.`

*IMPORTANT: BE EXACT!! And rename ALL OF YOUR ACCOUNTS IN THE BUDGET -> OR IT WONT WORK*

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

