"""views.py"""
# import os
# import json
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# import requests
# from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
# import pandas as pd
import yfinance as yf
from bankaccount.models import BankAccount
from stockapp.forms import AccountForm
from .services import get_stock_data
from . import models, forms

matplotlib.use('Agg')
load_dotenv()


def home(request):
    """Home Page"""
    stocks = [('AAPL'), ('GOOG'), ('AMZN')]
    context = {
        'stocks': stocks,
        'success': True if stocks else False
    }
    return render(request, 'home.html', context)


def simple_plot(request):
    """starter plot"""
    x = np.linspace(0, 2 * np.pi, 200)
    y = np.sin(x)

    fig, ax = plt.subplots()
    print(fig)
    ax.plot(x, y)
    ax.set_title('Sine Wave')
    ax.set_xlabel('Z')
    ax.set_ylabel('Y')

    # Save to a string buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert to base64 for embedding in HTML
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    plt.close()  # Important: close the figure to free memory

    context = {'graphic': graphic}

    return render(request, 'plot_example.html', context)


def stock_chart(request):
    """starter stock chart"""
    data = get_stock_data(request)
    if data.get('success'):
        # Create sample data for demonstration
        dates = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        prices = [150.0, 152.5, 148.0, 155.0, data['close_price']]

        fig, ax = plt.subplots(figsize=(10, 6))
        print(fig)
        ax.plot(dates, prices, marker='o', linewidth=2)
        ax.set_title(f'{data["symbol"]} Stock Price')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)

        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')
        plt.close()
        context = {'graphic': graphic, 'symbol': data['symbol']}
    else:
        context = {'error': 'No stock data available'}
    return render(request, 'plot_example.html', context)


def stock_lookup_ajax(request):
    """API endpoint for stock lookup"""
    symbol = request.GET.get('symbol', '').upper()
    if not symbol:
        return JsonResponse({'error': 'No symbol found.'})
    stock_info = get_stock_data(symbol)
    if not stock_info:
        return JsonResponse({'error': f'No {symbol} data found.', 'success': False})
    return JsonResponse({
        'success': True,
        'stock_info': stock_info
    })

@login_required
def dashboard(request):
    """User Dashboard"""
    bank_accounts = BankAccount.objects.filter(user=request.user)

    symbol = request.GET.get('symbol', '').upper() or None
    stock_info = {}
    error = None
    if symbol:
        stock_info = get_stock_data(symbol)
        if not stock_info:
            error = f'Could not find data for "{symbol}".'

    return render(request, 'dashboard.html', {
        'user': request.user,
        'stockapp_accounts': bank_accounts,
        'stock_info': stock_info,
        'symbol': symbol, 
        'error': error
    })


def logout_view(request):
    """User Logout"""
    logout(request)
    return redirect('home')


class LoginView(View):
    """Login view"""
    def get(self, request):
        """get form"""
        form = forms.LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        """create account"""
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            authenticated_user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('dashboard')
        return render(request, 'login.html', {'form': form})


class RegisterView(View):
    """register view"""
    def get(self, request):
        """get the view"""
        form = forms.LoginForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        """create account"""
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard')

        return render(request, 'register.html', {'form': form})


class AccountView(View):
    """account view"""
    def get(self, request):
        """get account"""
        form = forms.AccountForm()
        return render(request, 'account.html', {'form': form})

    def post(self, request):
        """create account"""
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Account information saved.")
        return render(request, 'account.html', {'form': form})

    def account_form(self, request):
        """account form"""
        if request.method == 'POST':
            form = forms.AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Account information saved.")
        else:
            form = forms.AccountForm()
        return render(request, 'account.html', {'form': form})


@login_required
def addaccount(request):
    """add an account"""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
        return redirect('dashboard')
    return render(request, 'account.html', {'form': AccountForm()})


class AccountListView(ListView):
    """account list view"""
    model = models.Account
    context_object_name = 'stockapp_accounts'
    def get_queryset(self):
        #only for currently logged in users
        return models.Account.objects.filter(user=self.request.user)

def portfolio_view(request):
    """List of tickers you want to display"""
    ticker_symbols = ["AAPL", "TSLA", "NVDA"]

    stocks_data = [] # This will hold the dictionaries for each stock

    for symbol in ticker_symbols:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        print('info', info)
        # Package only the data we need for each stock
        stock_details = {
            'symbol': symbol,
            'name': info.get('longName', 'N/A'),
            'price': info.get('currentPrice', 'N/A'),
            'change': info.get('regularMarketChangePercent', 0),
        }
        stocks_data.append(stock_details)

    context = {
        'stocks': stocks_data  # Pass the entire list to the template
    }

    return render(request, 'stock_list.html', context)
