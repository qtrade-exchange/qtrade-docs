import requests
import requests.auth
import base64
import time
import json
import binascii
from hashlib import sha256
from urllib.parse import urlparse


class QtradeAuth(requests.auth.AuthBase):

    def __init__(self, key):
        self.key_id, self.key = key.split(":")

    def __call__(self, req):
        # modify and return the request
        timestamp = str(int(time.time()))
        url_obj = urlparse(req.url)

        request_details = req.method + "\n"
        """
        request_details = 'GET
        '
        """
        uri = url_obj.path
        # uri = "/v1/user/orders"
        if url_obj.query:
            uri += "?" + url_obj.query
            # uri = "/v1/user/orders?open=true"
        request_details += uri + "\n"
        """
        request_details = 'GET
        /v1/user/orders?open=true
        '
        """
        request_details += timestamp + "\n"
        """
        request_details = 'GET
        /v1/user/orders?open=true
        1573604427
        '
        """
        if req.body:
            # this request has no body, so this code isn't run in this example
            if isinstance(req.body, str):
                request_details += req.body + "\n"
            else:
                request_details += req.body.decode('utf8') + "\n"
        else:
            request_details += "\n"
            """
            request_details = 'GET
            /v1/user/orders?open=true
            1573604427

            '
            """
        request_details += self.key
        """
        request_details = 'GET
        /v1/user/orders?open=true
        1573604427

        1111111111111111111111111111111111111111111111111111111111111111'
        """
        hsh = sha256(request_details.encode("utf8")).digest()
        signature = base64.b64encode(hsh)
        req.headers.update({
            "Authorization": "HMAC-SHA256 {}:{}".format(self.key_id, signature.decode("utf8")),
            "HMAC-Timestamp": timestamp
        })
        return req


# Create a session object to make repeated API calls easy!
api = requests.Session()
# Create an authenticator with your API key
api.auth = QtradeAuth("1:1111111111111111111111111111111111111111111111111111111111111111")

# Make a call to API
res = api.get('https://api.qtrade.io/v1/user/orders', params={'open': "true"}).json()
print(res)

# Generated headers are:
{'Accept': '*/*',
 'Accept-Encoding': 'gzip, deflate',
 'Authorization': 'HMAC-SHA256 1:111111111111111111111111111111111111111111',
 'Connection': 'keep-alive',
 'HMAC-Timestamp': '1574589817',
 'User-Agent': 'python-requests/2.18.4'}


# Generated body is:
{'data': {'orders': [{'created_at': '2019-11-12T22:42:15.643486Z',
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
                      'trades': None}]}}
