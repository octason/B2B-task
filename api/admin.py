from django.contrib import admin
from api.models import Wallet, Transaction


class TransactionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return Transaction.all_objects.all()


class WalletAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Wallet.all_objects.all()


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
