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

        if not currency_name or not amount or not user_account_id:
            return Response({"error": "Currency, Amount, and User Account are required fields."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Here we need to find the TotalAmount related to the specific currency
            total_amount, created = TotalAmount.objects.get_or_create(currency_name=currency_name)
            currency = Currency.objects.get(name=currency_name)
            user_account = UserAccount.objects.get(id=user_account_id)
        except Currency.DoesNotExist:
            return Response({"error": f"Currency '{currency_name}' does not exist."},
                            status=status.HTTP_400_BAD_REQUEST)
        except UserAccount.DoesNotExist:
            return Response({"error": "User Account not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            total_price = currency.price * amount
        except (ValueError, TypeError):
            return Response({"error": "Invalid amount provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if user_account.deduct_balance(total_price):
                if total_price >= 10:
                    print('Total price is greater than 10')
                    self.buy_from_exchange(currency_name, total_price + total_amount.total_amount)
                    total_amount.total_amount = 0  # Reset the total_amount to zero
                    total_amount.save()
                else:
                    print('Total price is less than 10')
                    total_amount.total_amount += total_price
                    total_amount.save()
                    if total_amount.total_amount >= 10:
                        self.buy_from_exchange(currency_name, total_amount.total_amount)
                        total_amount.total_amount = 0  # Reset the total_amount to zero
                        total_amount.save()

                order = Order.objects.create(
                    currency_name=currency,
                    amount=amount,
                    currency_price=total_price,
                    user_account=user_account
                )
                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An error occurred while processing the order: " + str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def buy_from_exchange(self, currency_name, amount):
        """
        A http request to buy a currency from exchange
        :param currency_name:
        :param amount:
        :return:
        """
        # Implement the logic to purchase from the external exchange
        print(f"Buying {currency_name} from exchange at total price {amount}")
        pass
