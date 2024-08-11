from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Currency, UserAccount, TotalAmount
from .serializers import OrderSerializer

class BuyOrderView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        currency_name = data.get('currency')
        amount = data.get('amount')
        user_account_id = data.get('user_account')

        try:
            # Here we need to find the TotalAmount related to the specific currency
            total_amount, created = TotalAmount.objects.get_or_create(currency_name=currency_name)
            currency = Currency.objects.get(name=currency_name)
            user_account = UserAccount.objects.get(id=user_account_id)
        except (Currency.DoesNotExist, UserAccount.DoesNotExist):
            return Response({"error": "Currency or User Account not found"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = currency.price * amount

        if total_price >= 10:
            self.buy_from_exchange(currency_name, total_price + total_amount.amount)
            total_amount.amount = 0  # Reset the total_amount to zero
            total_amount.save()  # Save the changes to the database
        else:
            total_amount.amount += total_price
            if total_amount.amount >= 10:
                self.buy_from_exchange(currency_name, total_amount.amount)
                total_amount.amount = 0  # Reset the total_amount to zero
                total_amount.save()  # Save the changes to the database

        if user_account.deduct_balance(total_price):
            order = Order.objects.create(
                currency=currency,
                amount=amount,
                price=total_price,
                user_account=user_account
            )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)


    def buy_from_exchange(self, currency_name, amount):
        """
        A http request to buy a currency from exchange
        :param currency_name:
        :param amount:
        :return:
        """
        # Implement the logic to purchase from the external exchange
        pass


