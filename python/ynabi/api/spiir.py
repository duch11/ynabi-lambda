import json
import glob
import shutil
import datetime

import requests
import re

from ynabi.model.transaction import Transaction
from ynabi.utils import string_to_datetime
from ynabi.api.logging import log
from .credentials import spiir_username, spiir_password



spiir_datetime_format = "%Y-%m-%dT%H:%M:%SZ"
tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)  # tomorrow
dawn_of_time = string_to_datetime("1000-01-01T00:00:00Z", spiir_datetime_format)

def _to_datetime(date_string):
    return string_to_datetime(date_string, spiir_datetime_format)


def _download_transactions():
    log("spiir"," get transactions")

    url_login = "https://mine.spiir.dk/log-ind"
    url_download = "https://mine.spiir.dk/Profile/ExportAllPostingsToJson"

    payload = {"Email": spiir_username, "Password": spiir_password}

    with requests.Session() as s:
        # Get RequestVerficationToken
        login_response = s.get(url_login)
        # Extract token using regex
        match = re.search(r'name="__RequestVerificationToken" type="hidden" value="(.*?)"', login_response.text)
        token = match.group(1) if match else ""
        print("token:", token)
        payload["__RequestVerificationToken"] = token
        s.post(url_login, data=payload)
        resp = s.get(url_download)

    return resp.json()


def _cached_transactions(transactions_local):
    if transactions_local is not None:
        log("spiir"," transactions_local already there")
        return transactions_local
    
    log("spiir"," transactions_local is None")
    transactions_local = _download_transactions()
    #log("spiir:", " transactions_local:", transactions_local)
    return transactions_local


def getTransactions(until_t=tomorrow, from_t=dawn_of_time, id_postfix="", use_cache=False):
    transactions_local = None
    """
    Returns list of Transation objects from raw transactions.
    Before and after time formatted as "2018-01-01T00:00:00Z".
    """
    #is string? make it a datetime!
    if isinstance(until_t, str):
        until_t = _to_datetime(until_t)

    #is string? make it a datetime!
    if isinstance(from_t, str):
        from_t = _to_datetime(from_t)
    
    transactions_local = _cached_transactions(transactions_local)
    filtered_transactions = [
        Transaction.from_spiir_dict(spiir_dict, id_postfix)
        for spiir_dict in _cached_transactions(transactions_local)
        if from_t < _to_datetime(spiir_dict["Date"]) <= until_t
    ]
    log("spiir.getTransactions -> earliest found",filtered_transactions[0].date)
    log("spiir.getTransactions -> latest   found", filtered_transactions[-1].date)
    return filtered_transactions


def accounts(transactions_local):
    accounts = []
    for transaction in _cached_transactions(transactions_local):
        accounts.append(transaction["AccountName"])
    return list(set(accounts))


def categories(transactions_local):
    categories = []
    for transaction in _cached_transactions(transactions_local):
        categories.append(transaction["CategoryName"])
    return list(set(categories))