from django.shortcuts import render
from .models import Account, Transaction
# Create your views here.
def account_list(request):
    if request.GET.get('search'):
        accounts = Account.objects.filter(name__icontains=request.GET.get('search'))
    else:
        accounts = Account.objects.all()
    return render(request, 'accounts/list.html', {'accounts': accounts})