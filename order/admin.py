from django.contrib import admin
from .models import UserAccount, Currency, TotalAmount, Order


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')  # Columns to display in the list view
    search_fields = ('user__username',)  # Fields to search by


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


class TotalAmountAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'total_amount')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_account', 'currency_name', 'amount', 'timestamp')
    list_filter = ('timestamp',)  # Add a filter by timestamp in the admin
    search_fields = ('user_account', 'currency_name__name')  # Fields to search by


# Register your models with the custom admin classes
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(TotalAmount, TotalAmountAdmin)
admin.site.register(Order, OrderAdmin)
