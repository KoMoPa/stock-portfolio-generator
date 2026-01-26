from django.urls import path
from . import views

app_name = 'bankaccount'

urlpatterns = [
    path('', views.home, name='home'),
]
