from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
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
        transactions = Transaction.objects.filter(Q(sender__name__icontains=request.GET.get('search'))|Q(receiver__name__icontains=request.GET.get('search')))
    else:
        transactions = Transaction.objects.filter(Q(sender=account)|Q(receiver=account))

    return render(request, 'accounts/detail.html', {'account': account, 'transactions': transactions, 'page':'account_detail'})

def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:account_list')  # Redirect to your home page
    else:
        form = AccountForm()
    return render(request, 'accounts/create_account.html', {'form': form})

def transaction_create(request, pk):
    accounts = Account.objects.filter(~Q(id=pk))
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(id=pk)
            if form.cleaned_data['amount'] == 0 or (account.balance - form.cleaned_data['amount']) < 0:
                messages.error(request, f"amount can't be zero or account balance not enough.")
                return redirect('accounts:transaction_create', pk)

            account.balance -= form.cleaned_data['amount']
            account.save()
            transaction = form.save(commit=False)
            transaction.sender = account
            transaction.save()
            receiver = form.cleaned_data['receiver']
            receiver.balance += form.cleaned_data['amount']
            receiver.save()
            return redirect('accounts:account_detail', pk)
        else:
            # Form is not valid; display errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = TransactionForm()
    return render(request, 'accounts/create_transaction.html', {'form': form, 'accounts': accounts})