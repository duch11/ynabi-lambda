import logging
from sys import stdout

from ynabi.api import spiir, ynab
from ynabi.model.transaction import Transaction
from ynabi.api.logging import log

from ynabi.config import start_date, id_postfix

def lambda_handler(event, context):   
    transactions_local = None
    log(event, context)

    log("============== ynabi-lambda v1.1.0 - start ==============")

    log("ynabi: importing spiir transactions to ynab")
    log(f"ynabi: including transaction after {start_date}")
    log(f"ynabi: using transaction id postfix {id_postfix}")

    # Spiir accounts
    log("Spiir accounts: ", spiir.accounts(transactions_local))

    # 1. Load data from Spiir (list of Transaction)
    transactions = spiir.getTransactions(
        from_t=start_date, id_postfix=id_postfix
    )

    # 2. Save transactions to YNAB
    ynab.create_transactions(transactions)

    log("============== ynabi v1.0 - end ==============")

    return {
        'statusCode': 200,
        'body': "OK"
    }

if __name__ == "__main__":
    logger = logging.getLogger()

    streamHandler = logging.StreamHandler(stdout)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.INFO)
    print(lambda_handler("hej", "hej"))