from qtrade_client.api import QtradeAPI

# Create an API client with your key
endpoint = "https://api.qtrade.io"
key = "1:1111111111111111111111111111111111111111111111111111111111111111"
api = QtradeAPI(endpoint, key)

# Make a call to API
res = api.orders(open=True)
print(res)

# Returned list:
[{'created_at': '2019-11-12T22:42:15.643486Z',
  'id': 8932525,
  'market_amount': '1.10428011',
  'market_amount_remaining': '1.10428011',
  'market_id': 1,
  'open': True,
  'order_type': 'sell_limit',
  'price': '0.0083759',
  'trades': None},
 {'created_at': '2019-11-12T22:42:14.713136Z',
  'id': 8932523,
  'market_amount': '0.92023342',
  'market_amount_remaining': '0.92023342',
  'market_id': 1,
  'open': True,
  'order_type': 'sell_limit',
  'price': '0.00788731',
  'trades': None},
 {'base_amount': '0.00433166',
  'created_at': '2019-11-12T22:42:08.51142Z',
  'id': 8932503,
  'market_amount': '14862.44638875',
  'market_amount_remaining': '14862.44638875',
  'market_id': 36,
  'open': True,
  'order_type': 'buy_limit',
  'price': '0.00000029',
  'trades': None}]
