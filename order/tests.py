import pytest
import rest_framework.exceptions
from order.views import BuyOrderView


@pytest.mark.parametrize(
    'currency_name, amount, user_account',
    ['ABAN', 3, "1"]
)
def test_buy_currency(currency_name, amount, user_account):
    data = {
        'currency_name': currency_name,
        'amount': amount,
        'user_account': user_account
    }
    expected_data = {
        "currency_name": "ABAN",
        "amount": "1.00000000",
        "currency_price": "4.00000000",
        "user_account": "fatemeh - Balance: 924.00",
        "timestamp": "2024-08-13T04:49:05.491280Z"
    }
    actual_data = BuyOrderView(data)
    assert actual_data == expected_data
