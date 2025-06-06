import json

from ynabi.api import ynab
from ynabi.api.logging import log


class Transaction:
    def __init__(
        self,
        account_id=None,
        date=None,
        amount=None,
        payee_id=None,
        payee_name=None,
        category_id=None,
        memo=None,
        cleared=None,
        approved=None,
        flag_color=None,
        import_id=None,
    ):
        self.account_id = account_id  # string
        self.date = date  # string
        self.amount = amount  # 0
        self.payee_id = payee_id  # string
        self.payee_name = payee_name  # string, len <= 50
        self.category_id = category_id  # string
        self.memo = memo  # string
        self.cleared = cleared  # cleared | uncleared | reconciled
        self.approved = approved  # true
        self.flag_color = flag_color  # red
        self.import_id = import_id  # string

    @classmethod
    def from_spiir_dict(cls, spiir_dict, id_postfix=""):
        #ynab_category_id = ynab.get_category_id(spiir_dict["CategoryName"])

        #if spiir_dict["CategoryName"] is not None and ynab_category_id == None:
        #    log(
        #        "warning: unknown ynab category ({}), transaction will be uncategorized".format(
        #            spiir_dict["CategoryName"]
        #        )
        #    )

        return cls(
            account_id=ynab.get_account_id(spiir_dict["AccountName"]),
            date=spiir_dict["Date"],
            amount=int(spiir_dict["Amount"] * 1000.0),
            payee_id=None,
            payee_name=spiir_dict["Description"][:50],
            category_id=None,
            memo=None,
            cleared="cleared",
            approved=False,
            flag_color=None,
            import_id=spiir_dict["Id"] + id_postfix,
        )

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "date": self.date,
            "amount": self.amount,
            "payee_id": self.payee_id,
            "payee_name": self.payee_name,
            "category_id": self.category_id,
            "memo": self.memo,
            "cleared": self.cleared,
            "approved": self.approved,
            "flag_color": self.flag_color,
            "import_id": self.import_id,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return f"""Transaction(
    "account_id": {self.account_id},
    "date": {self.date},
    "amount": {self.amount},
    "payee_id": {self.payee_id},
    "payee_name": {self.payee_name},
    "category_id": {self.category_id},
    "memo": {self.memo},
    "cleared": {self.cleared},
    "approved": {self.approved},
    "flag_color": {self.flag_color},
    "import_id": {self.import_id},
)"""
