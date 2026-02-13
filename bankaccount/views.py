# bank_accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankAccount, Transaction
from .forms import TransactionForm
from stockapp.forms import AccountForm

# Create your views here.
def home(request):
    return render(request, 'bankaccount/home.html')


@login_required
def bank_account_list(request):
    """List all bank accounts for a user"""
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'bankaccount/bank_account_list.html', {'accounts': accounts})


@login_required
def bank_account_create(request):
    """Create a new bank account"""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('bankaccount:bank_account_list')
        else:
            messages.error(request, 'Please correct errors.')
    else:
        form = AccountForm()
    return render(request, 'account.html', {'form': form})


@login_required
def bank_account_detail(request, pk):
    """Get details of an existing bank account"""
    account = get_object_or_404(BankAccount, pk=pk, user=request.user)
    # alternate transaction lookup
    # transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
    transactions = account.transactions.order_by('-timestamp')
    return render(request, 'bankaccount/detail.html', {
        'account': account,
        'transactions': transactions
    })


@login_required
def bank_account_deposit(request, pk):
    """Deposit to an existing bank account"""
    account = get_object_or_404(BankAccount, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account.deposit(form.cleaned_data['amount'])
            messages.success(request, 'Deposit successful.')
            return redirect('bankaccount:bank_account_detail', pk=pk)
        else:
            messages.error(request, 'Invalid amount.')
    else:
        form = TransactionForm()
    return render(request, 'bankaccount/deposit.html', {'account': account, 'form': form})


@login_required
def bank_account_withdraw(request, pk):
    """Withdraw from an existing bank account"""
    account = get_object_or_404(BankAccount, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            account.withdrawal(form.cleaned_data['amount'])
            messages.success(request, 'Withdrawal successful.')
            return redirect('bankaccount:bank_account_detail', pk=pk)
        else:
            messages.error(request, 'Invalid amount.')
    else:
        form = TransactionForm()
    return render(request, 'bankaccount/withdraw.html', {'account': account, 'form': form})


@login_required
def bank_account_delete(request, pk):
    """Delete an existing bank account"""
    account = get_object_or_404(BankAccount, pk=pk, user=request.user)

    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Deleted successfully.')
        return redirect('bankaccount:bank_account_list')
    return render(request, 'bankaccount/delete.html', {'account': account})

