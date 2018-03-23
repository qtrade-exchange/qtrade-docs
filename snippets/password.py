import requests
import base64
import time
import json
import binascii
from hashlib import sha256

api = requests.Session()
res = api.post('{{ url }}v1/login',
        json={"email": "test@gmail.com", "password": "test12345"}).json()
api.headers.update({"Authorization": "Bearer {}".format(res['token'])})
res = api.get('{{ url }}/v1/user/me').json()
