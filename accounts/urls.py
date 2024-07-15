from django.urls import path
from .views import account_list, account_detail, account_create, transaction_create

app_name = 'accounts'
urlpatterns = [
    path('accounts/create', account_create, name='account_create'),
    path('<uuid:pk>/transactions/create', transaction_create, name='transaction_create'),
    path('<uuid:pk>', account_detail, name='account_detail'),
    path('', account_list, name='account_list'),
]