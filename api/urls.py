from rest_framework.routers import DefaultRouter
from api.views import WalletViewSet, TransactionViewSet

router_v1 = DefaultRouter()

router_v1.register(r"wallets", WalletViewSet, basename="wallet")
router_v1.register(r"transactions", TransactionViewSet, basename="transcation")
