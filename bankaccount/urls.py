from django.urls import path
from . import views

app_name = 'bankaccount'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.bank_account_create, name='bank_account_create'),
    path('deposit/<uuid:pk>/', views.bank_account_deposit, name='bank_account_deposit'),
    path('withdraw/<uuid:pk>/', views.bank_account_withdraw, name='bank_account_withdraw'),
    path('detail/<uuid:pk>/', views.bank_account_detail, name='bank_account_detail'),
    path('delete/<uuid:pk>/', views.bank_account_delete, name='bank_account_delete'),
]
