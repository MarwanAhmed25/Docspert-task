from django.urls import path
from .views import account_list, account_detail

app_name = 'accounts'
urlpatterns = [
    path('', account_list, name='account_list'),
    path('/<uuid:pk>', account_detail, name='account_detail'),
]