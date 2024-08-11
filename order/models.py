from django.db import models
from django.contrib.auth.models import User


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relationship with the User model
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)  # Account balance

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True)  # Cryptocurrency name
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)  # Cryptocurrency price

    def __str__(self):
        return self.name


class TotalAmount(models.Model):
    currency_name = models.ForeignKey(Currency, on_delete=models.CASCADE)  # Foreign key to the Currency model
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)  # Total amount accumulated


class Order(models.Model):
    currency_name = models.ForeignKey(Currency, on_delete=models.CASCADE)  # Cryptocurrency name
    amount = models.DecimalField(max_digits=20, decimal_places=8)  # Amount of cryptocurrency
    price = models.ForeignKey(Currency, on_delete=models.CASCADE)  # Purchase price of cryptocurrency
    user_account = models.CharField(max_length=100)  # User account
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for the order

    def __str__(self):
        return f"{self.user_account} - {self.currency_name.name} - {self.amount}"

