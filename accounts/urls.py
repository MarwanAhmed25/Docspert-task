from django.urls import path
from .views import account_list

app_name = 'accounts'
urlpatterns = [
    path('', account_list, name='account_list'),
]