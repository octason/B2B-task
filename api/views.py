from rest_framework.viewsets import ModelViewSet
from api.serializers import TransactionSerializer, WalletSerializer
from api.models import Transaction, Wallet
from rest_framework_json_api.schemas.openapi import AutoSchema
from api.services import TransactionService
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError


class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (permissions.AllowAny,)

    schema = AutoSchema
    search_fields = ["label"]
    ordering_fields = ["id", "label", "balance"]
    ordering = ["id"]


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = TransactionSerializer
    schema = AutoSchema
    search_fields = ["txid"]
    ordering_fields = ["id", "amount"]
    ordering = ["id"]

    def update(self, request, *args, **kwargs):
        # Transactions cannot be updated if they are in blockchain
        return Response(
            {"detail": "Updating transactions is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Partially updating transactions is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def create(self, request, *args, **kwargs) -> Response:
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        wallet = validated_data.get("wallet")
        txid = validated_data.get("txid")
        amount = validated_data.get("amount")

        try:
            transaction_service = TransactionService(wallet)
            transaction = transaction_service.create_tx(txid, amount)
            serializer = self.get_serializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
