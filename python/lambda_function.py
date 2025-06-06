import logging
from sys import stdout

from ynabi.api import spiir, ynab
from ynabi.model.transaction import Transaction
from ynabi.api.logging import log

from ynabi.config import start_date, id_postfix

def lambda_handler(event, context):   
    log(event, context)
    
    # DEBUG Spiir accounts and categories
    
    ### transactions_local = None
    ### log("Spiir accounts", spiir.accounts(transactions_local))
    ### log("Spiir Categories", spiir.categories(transactions_local))
    
    log("============== ynabi v1.0 - start ==============")

    log("lambda_handler","importing spiir transactions to ynab")
    log("lambda_handler",f"including transaction after {start_date}")
    log("lambda_handler",f"using transaction id postfix {id_postfix}")

    # 1. Load data from Spiir (list of Transaction)
    transactions = spiir.getTransactions(
        from_t=start_date, id_postfix=id_postfix
    )  
    
    # 2. Save transactions to YNAB
    ynab.create_transactions(transactions)
    
    log("============== ynabi v1.0 - end ==============")
    return {
        'statusCode': 200,
        'body': "OK",
        'message': "No message"
    }

if __name__ == "__main__":
    lambda_handler("an jonas event", "jonas context")