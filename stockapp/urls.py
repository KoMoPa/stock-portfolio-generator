from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('account/', views.addaccount, name='addaccount'),
    # path('plot/', views.stock_chart, name='simpleplot'),
    # path('plot/', views.simple_plot, name='simpleplot'),
    # path('stock-lookup/', views.stock_lookup, name='stocklookup'),
    # path('portfolio/', views.portfolio_view, name='portfolio'),
    path('api/stock-lookup/', views.stock_lookup_ajax, name='stock_lookup_ajax'),
]
