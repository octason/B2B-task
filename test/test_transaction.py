import pytest
from decimal import Decimal
from mixer.backend.django import mixer
from api.models import Wallet, Transaction
from api.serializers import WalletSerializer
from rest_framework.exceptions import ValidationError
from api.services import TransactionService
from django.db import IntegrityError


@pytest.fixture
def wallet():
    return mixer.blend(Wallet)


@pytest.fixture
def transaction():
    return mixer.blend(Transaction)


@pytest.mark.django_db
def test_transaction_create(wallet):
    service = TransactionService(wallet)
    old_balance = wallet.balance

    txid = mixer.faker.pystr(min_chars=10, max_chars=255)
    amount = Decimal("10.0")
    transaction = service.create_tx(txid, amount)

    assert transaction.id is not None
    assert wallet.balance != old_balance
    assert transaction.wallet.id == wallet.id

    amount = Decimal("-10.0")
    txid = mixer.faker.pystr(min_chars=10, max_chars=255)

    transaction = service.create_tx(txid, amount)
    assert transaction.id is not None
    assert wallet.balance == old_balance
    assert transaction.wallet.id == wallet.id


@pytest.mark.django_db
def test_create_positive_balance_wallet():
    label = mixer.faker.pystr(min_chars=10, max_chars=255)
    balance = Decimal(
        mixer.faker.pydecimal(left_digits=4, right_digits=18, positive=True)
    )
    wallet_data = {
        "label": label,
        "balance": balance,
    }
    serializer = WalletSerializer(data=wallet_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    instance = serializer.instance

    assert instance.id is not None
    assert instance.balance == balance
    assert instance.label == label


@pytest.mark.django_db
def test_create_negative_balance_wallet():
    label = mixer.faker.pystr(min_chars=10, max_chars=255)
    balance = Decimal(
        mixer.faker.pydecimal(left_digits=4, right_digits=18, positive=True)
    )

    negative_balance = balance.copy_negate()
    wallet_data = {
        "label": label,
        "balance": negative_balance,
    }
    serializer = WalletSerializer(data=wallet_data)

    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    assert "balance" in excinfo.value.detail
    assert excinfo.value.detail["balance"] == ["The balance cannot be negative."]


@pytest.mark.django_db
def test_create_transaction_with_not_enough_balance():
    wallet = mixer.blend(Wallet, balance=Decimal("100.00"))
    old_balance = wallet.balance
    service = TransactionService(wallet)
    all_transactions_count = Transaction.objects.all().count()
    txid = mixer.faker.pystr(min_chars=10, max_chars=255)
    exceeding_amount = Decimal("-101.00")

    with pytest.raises(ValidationError) as excinfo:
        service.create_tx(txid, exceeding_amount)
    assert excinfo.value.detail == ["Insufficient balance for this transaction."]

    # Check if balance keep the same
    assert wallet.balance == old_balance

    # Check if transactions creation aborted

    assert all_transactions_count == Transaction.objects.all().count()


@pytest.mark.django_db
def test_unique_transactions(wallet):
    txid_test_str = "Test"
    amount = Decimal("100.00")

    service = TransactionService(wallet)

    transaction = service.create_tx(txid_test_str, amount)

    assert transaction is not None
    assert transaction.id is not None
    assert Transaction.objects.filter(txid=txid_test_str).count() == 1

    with pytest.raises(IntegrityError):
        service.create_tx(txid_test_str, amount)

    assert Transaction.objects.filter(txid=txid_test_str).count() == 1
