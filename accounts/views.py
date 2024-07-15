from django.shortcuts import render
from django.db.models import Q
from .models import Account, Transaction
# Create your views here.
def account_list(request):
    if request.GET.get('search'):
        accounts = Account.objects.filter(name__icontains=request.GET.get('search'))
    else:
        accounts = Account.objects.all()
    return render(request, 'accounts/list.html', {'accounts': accounts, 'page':'home'})

def account_detail(request, pk):
    account = Account.objects.get(pk=pk)
    if request.GET.get('search'):
        transactions = Transaction.objects.filter(Q(sender__name__icontains=request.GET.get('search')&
                         Q(receiver=account))|Q(receiver__name__icontains=request.GET.get('search')& Q(sender=account)))
    else:
        transactions = Transaction.objects.filter(Q(sender=account)|Q(receiver=account))

    return render(request, 'accounts/detail.html', {'account': account, 'transactions': transactions, 'page':'account_detail'})