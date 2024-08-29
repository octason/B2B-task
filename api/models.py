from django.db import models
from decimal import Decimal
from django.db.models import Q


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteMixin:
    # Do soft delete in case we need to keep wallet's data
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()


class Wallet(SoftDeleteMixin, models.Model):
    label = models.CharField("Label of the wallet", max_length=255)
    balance = models.DecimalField(
        "Balance of the Wallet",
        max_digits=30,
        decimal_places=18,
        default=Decimal("0.0"),
    )
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def hard_delete(self, using=None, keep_parents=False):
        super(Wallet, self).delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.label

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(balance__gte=0), name="balance_non_negative")
        ]
        indexes = [
            models.Index(fields=["label"]),
        ]


class Transaction(SoftDeleteMixin, models.Model):
    txid = models.CharField("Transaction ID", max_length=255, unique=True)

    amount = models.DecimalField(
        "Transaction Amount",
        max_digits=30,
        decimal_places=18,
    )
    wallet = models.ForeignKey("Wallet", on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=["txid"]),
        ]

    def __str__(self):
        return self.txid
