from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Account(models.Model):
    """Model for User Bank Account"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    account_type = models.CharField(max_length=20, choices=[('1', 'Checking'), ('2', 'Savings')], default='checking')

    def __str__(self):
        return f"{self.user.username}'s Account: ${self.balance:,.2f}"
    
    def __repr__(self):
        return f"Account: {self.user.username}  Balance: {self.balance:,.2f}"
    
    def deposit(self, amount):
        """Add funds to account"""
        if amount <= 0:
            raise ValueError("Must deposit poisitive amount.")
        self.balance += amount
        self.save()
        # Create a transaction record
        Transaction.objects.create(
            account=self,
            amount=amount,
            transaction_type='Deposit'
        )
        return self.balance

    def withdrawal(self, amount):
        """Subtract funds from account"""
        if amount <= 0:
            raise ValueError("Must withdraw positive amount.")
        if self.balance < amount:
            raise ValueError("Not enough money in account to withdraw this amount.")
        self.balance -= amount
        self.save()
        # Create a transaction record
        Transaction.objects.create(
            account=self,
            amount=amount,
            transaction_type='Withdrawal'
        )
        return self.balance

    def get_transaction_history(self):
        """return all transactions"""
        return self.transactions.all()


class Transaction(models.Model):
    """Model for Transaction"""
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Interest', 'Interest'),
        ('Fee', 'Fee')
    ]

    transaction_type = models.CharField(choices=TRANSACTION_TYPES)

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"${abs(self.amount):.2f} {'debit' if self.amount < 0 else 'credit'} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class Stock(models.Model):
    """Model for Stock"""
    name = models.CharField()
    ticker = models.CharField(max_length=5)
    # current_price = models.DecimalField(decimal_places=2)
    # purchase_prices = models.DecimalField(decimal_places=2)
    # quantity = models.DecimalField(decimal_places=2)

    # open = models.DecimalField(decimal_places=2)
    # high = models.DecimalField(decimal_places=2)
    # low = models.DecimalField(decimal_places=2)

    # def market_value
    # def book_cost
    # def gain_loss
    # def account_percentage
