import uuid
# from datetime import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction

User = get_user_model()

class BankAccount(models.Model):
    """class representing a bank account"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bankaccounts',
    )
    account_type = models.CharField()
    account_name = models.CharField()
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @db_transaction.atomic
    def deposit(self, amount):
        amount = abs(amount)

        Transaction.objects.create(
            account=self,
            amount=amount,
            transaction_type=Transaction.DEPOSIT,
            # timestamp=timezone.now(),
        )

        self.balance += amount
        self.save(update_fields=['balance'])


    @db_transaction.atomic
    def withdrawal(self, amount):
        amount = abs(amount)

        Transaction.objects.create(
            account=self,
            amount=amount,
            transaction_type=Transaction.WITHDRAWAL,
            # timestamp=timezone.now(),
        )

        self.balance -= amount
        self.save(update_fields=['balance'])

    def __str__(self):
        return f"${self.account_type}: {self.balance}"


class Transaction(models.Model):
    """class representing a transaction"""
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'
    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]
    transaction_type = models.CharField(choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    def __str__(self):
        return f"${self.transaction_type}: {self.amount} on {self.timestamp}"