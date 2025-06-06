import time
import json
import requests
from ynabi.api.logging import log, err


from .credentials import ynab_api_token, ynab_budget_id

api = "https://api.youneedabudget.com/v1/"
headers = {"Authorization": "Bearer {}".format(ynab_api_token)}

#
# Requests
#
def get_accounts():
    url = api + f"budgets/{ynab_budget_id}/accounts"
    resp = requests.get(url, headers=headers)
    return resp.json()["data"]["accounts"]


def get_category_groups():
    url = api + f"budgets/{ynab_budget_id}/categories"
    resp = requests.get(url, headers=headers)
    return resp.json()["data"]["category_groups"]

def get_transactions(since_date):
    url = api + f"budgets/{ynab_budget_id}/transactions?since_date={since_date}"
    resp = requests.get(url, headers=headers)
    
    try:
        data = resp.json()
    except ValueError:
        raise Exception("Response is not valid JSON")

    log("ynab.get_transactions", resp)
    
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {data}")

    if "data" not in data or "transactions" not in data["data"]:
        raise Exception(f"Unexpected response format: {data}")
    
    
    return data["data"]["transactions"]


def create_transactions(transactions, chunk_size=100):
    """
    Uploads transactions to YNAB. No return value.
    """
    url = api + f"/budgets/{ynab_budget_id}/transactions/bulk"

    if len(transactions) == 0:
        log("ynab", "no transactions to upload")
        return

    # Just go with it.. it basically makes chunks of transactions.. 
    # first a slice, but that is done in the for loop, because its list comprehension
    # F*** python
    chunks = [
        transactions[x : x + chunk_size]
        for x in range(0, len(transactions), chunk_size)
    ]

    log("ynab:",f"creating {len(transactions)} transactions in {len(chunks)} chunks")
    from ynabi.config import start_date
    ynab_transactions = get_transactions(start_date)

    for i, chunk in enumerate(chunks):
        valid_transactions = [
                single_transaction.to_dict() 
                for single_transaction in chunk
                if single_transaction.import_id not in [t["import_id"] for t in ynab_transactions]
            ]
        id_from_ynab = ynab_transactions[0]["import_id"]
        id_from_spiir = chunk[0].import_id
                
        body = {"transactions": 
            [
                single_transaction.to_dict() 
                for single_transaction in chunk
            ]
        }
        
        log("ynab",f"posting transaction chunk {i+1}/{len(chunks)}.. ")

        # log each transaction id
\
        resp = requests.post(url, json=body, headers=headers)
        if not 200 <= resp.status_code < 300:
            err("ynab error", f"bulk create request failed ({resp.status_code})", resp.request.body, resp.json())
        
        response_data = resp.json()["data"]["bulk"]
    
    log("ynab: done")

    return


#
# Cache
#
_ynab_accounts = None
_ynab_category_groups = None


def clear_cache():
    global _ynab_accounts
    global _ynab_category_groups
    _ynab_accounts = None
    _ynab_category_groups = None


def accounts():
    global _ynab_accounts
    if _ynab_accounts is None:
        _ynab_accounts = get_accounts()
    return _ynab_accounts


def category_groups():
    global _ynab_category_groups
    if _ynab_category_groups is None:
        _ynab_category_groups = get_category_groups()
    return _ynab_category_groups


#
# Lookups
#
def get_account_id(name):
    for account in accounts():
        if name == account["name"]:
            return account["id"]


def get_category_id(name):
    for category_group in category_groups():
        for category in category_group["categories"]:
            if name == category["name"]:
                return category["id"]
