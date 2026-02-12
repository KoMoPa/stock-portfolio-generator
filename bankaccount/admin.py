"""bank account admin exposure"""
from django.contrib import admin
from .models import BankAccount, Transaction

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    """admin bank account view"""
    list_display = ('account_name', 'user', 'account_type', 'balance', 'created_at')
    list_filter = ('account_type', 'created_at', 'user')
    search_fields = ('account_name', 'user__username')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Account Info', {
            'fields': ('user', 'account_name', 'account_type')
        }),
        ('Balance', {
            'fields': ('balance',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    readonly_fields = ('timestamp',)