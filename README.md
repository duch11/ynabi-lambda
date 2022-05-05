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

## Credentials

Add the following to `python/ynabi/api/credentials.py`

```bash
# Spiir
spiir_username = "" # Used for logging in to Spiir: www.mine.spiir.dk/log-ind
spiir_password = ""

# YNAB
ynab_api_token = "" # Get it here => https://api.youneedabudget.com/#personal-access-tokens
ynab_budget_id = "" # Get it from budget-URL ie: `https://app.youneedabudget.com/YOUR-BUDGET-ID-IS-HERE/budget`
```


## YNAB Bank Account Names

**🛑IMPORTANT🛑**
1. Account names must match exactly. 
2. 3 Account in Spiir => 3 Account in YNAB

```
Examples:
Spiir Accounts  | YNAB Accounts
--------------------------------------------
- Dankort       | - Dankort   <<< GOOD
- Savings       | - Savings   <<< GOOD (both accounts match)
--------------------------------------------
- Mastercard    | - MCard     <<< WRONG Name
- Savings       | - Savings   <<< WRONG (only 1 account matches)

```

## Installation

### Requirements

- Python 3.8 or above

### How to

0. Clone this repo.
1. Do the required configuration above
2. `py -m venv venv`
3. `pip install requests`
4. `py ./lambda/lambda_function.py`



# Terraform Deployment on AWS Lambda (optional)

*Warning: AWS/cloud setup, requires an AWS account and basic knowledge about Amazon Web Services.* 

0. Edit Credentials and Rename YNAB bank account names as described above
1. See ./terraform/README.md for more.. 

### In case of issues:

See AWS documentation: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

