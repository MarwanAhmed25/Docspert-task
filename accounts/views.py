from django.shortcuts import render
from .models import Account, Transaction
# Create your views here.
def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/list.html', {'accounts': accounts})