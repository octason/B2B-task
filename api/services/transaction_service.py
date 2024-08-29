from django.db import transaction
from rest_framework.exceptions import ValidationError
from api.models import Wallet, Transaction
from decimal import Decimal


class TransactionService:
    def __init__(self, wallet: Wallet) -> None:
        self.wallet = wallet

    @transaction.atomic
    def create_tx(self, txid: str, amount: Decimal) -> Transaction:
        new_balance = self.wallet.balance + amount

        if new_balance < 0:
            raise ValidationError("Insufficient balance for this transaction.")

        self.wallet.balance = new_balance
        self.wallet.save()

        transaction = Transaction.objects.create(
            wallet=self.wallet, txid=txid, amount=amount
        )

        return transaction
