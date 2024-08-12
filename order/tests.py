from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Currency, UserAccount, Order, TotalAmount

class BuyOrderViewTest(APITestCase):

    def setUp(self):
        # ایجاد داده‌های اولیه برای تست‌ها
        self.currency = Currency.objects.create(name="ABAN", price=4)
        self.user_account = UserAccount.objects.create(id=1, balance=100)
        self.url = reverse('buy-order')  # فرض می‌کنیم نام url ویو 'buy-order' است

    def test_successful_order(self):
        data = {
            "currency": "ABAN",
            "amount": 2,  # قیمت کل = 4 * 2 = 8
            "user_account": self.user_account.id
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().currency_name, self.currency)
        self.assertEqual(Order.objects.get().amount, 2)
        self.assertEqual(Order.objects.get().currency_price, 8)

    def test_insufficient_balance(self):
        data = {
            "currency": "ABAN",
            "amount": 30,  # قیمت کل = 4 * 30 = 120 (بیشتر از موجودی کاربر)
            "user_account": self.user_account.id
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Insufficient balance")
        self.assertEqual(Order.objects.count(), 0)

    def test_invalid_currency(self):
        data = {
            "currency": "INVALID_CURRENCY",  # ارزی که وجود ندارد
            "amount": 2,
            "user_account": self.user_account.id
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Currency 'INVALID_CURRENCY' does not exist.")
        self.assertEqual(Order.objects.count(), 0)

    def test_invalid_user_account(self):
        data = {
            "currency": "ABAN",
            "amount": 2,
            "user_account": 9999  # شناسه حساب کاربری که وجود ندارد
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "User Account not found.")
        self.assertEqual(Order.objects.count(), 0)

    def test_total_amount_less_than_10(self):
        data = {
            "currency": "ABAN",
            "amount": 2,  # قیمت کل = 4 * 2 = 8 (کمتر از 10)
            "user_account": self.user_account.id
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        total_amount = TotalAmount.objects.get(currency_name="ABAN")
        self.assertEqual(total_amount.total_amount, 8)  # TotalAmount باید 8 باشد

    def test_total_amount_greater_than_10(self):
        # ابتدا یک TotalAmount ایجاد می‌کنیم
        TotalAmount.objects.create(currency_name="ABAN", total_amount=5)

        data = {
            "currency": "ABAN",
            "amount": 2,  # قیمت کل = 4 * 2 = 8 (که باید مجموع total_amount را به بالای 10 برساند)
            "user_account": self.user_account.id
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        total_amount = TotalAmount.objects.get(currency_name="ABAN")
        self.assertEqual(total_amount.total_amount, 0)  # TotalAmount باید ریست شده و 0 باشد

# python manage.py test
