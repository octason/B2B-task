from rest_framework_json_api.serializers import ModelSerializer, ValidationError
from api.models import Wallet, Transaction
from typing import OrderedDict, Any


class SoftDeleteSerializerMixin:
    def to_representation(self, instance: Wallet) -> OrderedDict[str, Any]:
        representation = super().to_representation(instance)

        if not instance.is_deleted:
            representation.pop("is_deleted")
        return representation


class WalletSerializer(SoftDeleteSerializerMixin, ModelSerializer):
    def validate_balance(self, value):
        """
        Check that the balance is positive.
        """
        if value < 0:
            raise ValidationError("The balance cannot be negative.")
        return value

    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionSerializer(SoftDeleteSerializerMixin, ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
