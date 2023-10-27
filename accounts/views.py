from rest_framework.generics import ListCreateAPIView

from accounts.models import Account
from accounts.serializers import AccountSerializer


# Create your views here.
class AccountView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
