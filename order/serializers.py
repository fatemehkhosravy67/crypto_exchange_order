from rest_framework import serializers
from .models import UserAccount, Currency, TotalAmount, Order


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['user', 'balance']  # Specify the fields you want to include


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'price']


class TotalAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalAmount
        fields = ['currency_name', 'total_amount']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['currency_name', 'amount', 'currency_price', 'user_account', 'timestamp']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
