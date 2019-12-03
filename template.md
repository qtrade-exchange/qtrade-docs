---
title: qTrade API Docs

language_tabs: # must be one of https://git.io/vQNgJ
  - python--Python: Python
  - python--PyClient: Py Client
  - javascript: Node.js
  - php
  - shell

toc_footers:
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true
---

# Introduction

Welcome to the qTrade API documentation. These documents detail how to use qTrade's exchange API and are open source [on github](https://github.com/qtrade-exchange/qtrade-docs). If you'd like to make a correction or suggest any changes please feel free to make a pull request.

qTrade's APIs are separated into two categories public and private. Private APIs require authentication and allows placing orders, making deposits and withdrawals, and other account information. Public APIs provide market data and do not require authentication.

The qTrade API is available at 

`https://api.qtrade.io/`


<aside class="info">
  All URL endpoints are prefixed with the API version. Try this URL in your browser: <code>https://api.qtrade.io/v1/tickers</code>
</aside>


# Client Libraries

### Python Client
We provide a [Python client](https://github.com/qtrade-exchange/qtrade-py-client) for our API.  This client offers helper functions, convenient response formatting, and automatic rate limit waiting to make developing applications with our API as efficient as possible.

### CryptoCurrency eXchange Trading Library
Our API is also supported by [CCXT](https://github.com/ccxt/ccxt), a JavaScript / Python / PHP cryptocurrency trading API with support for over 120 exchanges.


# Vocabulary

Here is how we define the terms used in our documentation and API:

Term | Definition
--- | ---
Market Currency | The currency which is bought or sold on a market (e.g. NYZO on the NYZO/BTC market).
Base Currency | The currency which is used to buy or sell a market currency (currently BTC on all markets).  Price is given in this currency.
Value | The total worth of an order or trade in base currency.
Amount | The size of an order or trade in market currency.


# Authentication

``` python--Python
{{ load_snippet('hmac.py') }}
```
``` python--PyClient
{{ load_snippet('hmac_client.py') }}
```
``` javascript
{{ load_snippet('hmac.js') }}
```
``` php
{{ load_snippet('hmac.php')}}
```

qTrade's private API requires HMAC authentication. All requests and responses are the `application/json` content type return typical HTTP status codes.

The HMAC protocol uses an API key issued on qTrade's website in the account settings page. API keys have a limited set of permissions and you should always issue a key with the minimum set of permissions needed. API keys may also be revoked on the settings page.

API Key permissions are mapped into `realms` and each `realm` is granted access to specific API endpoints

Realm | Endpoints 
--- | --- 
Info | `/user/balances`, `/user/withdraws`, `/user/deposits`, `/user/orders`
Withdraw | `/user/withdraw`
Deposit | `/user/deposit_address/{currency_code}` 
Trade | `/user/sell_limit`, `/user/buy_limit`, `/user/cancel_order`


# Approved Withdraw Addresses

For user security, account withdrawals require email or 2FA approval.  However, this usually isn't practical for API integrations.

Users can whitelist specific withdrawal addresses in the [Manage Addresses panel](https://qtrade.io/settings/manage_addresses) of the user settings on the website.  Adding an address to the approved list will allow users and API integrations to withdraw to it without manual confirmation.

<aside class="warning">

Any user or API with access to the account can withdraw to approved addresses with NO CONFIRMATION.  Only approve addresses of wallets you control.

</aside>

{% macro endpoint(item) %}
## {{ item.name }}



{% for resp in item.response %}

{% if item.request.method == "POST" and resp.request.body %}

{% if resp.python_client_example %}
``` python--PyClient
{{ resp.python_client_example }}
```
{% endif %}
``` python--Python
{% if resp.python_example %}
{{ resp.python_example }}
{% else %}
req = {{ resp.request.body | json_to_python_dict }}
api.post("{{ resp.request.url.path }}", json=req).json()
{% endif %}
```
``` javascript
req = {{ resp.request.body | json_to_python_dict }}
api.post("{{ resp.request.url.path }}", JSON.stringify(req), (resp) => {})
```
``` php
<?php
$req = {{ resp.request.body | json_to_php_array }}
$result = $api->post("{{ resp.request.url.path }}", json_encode($req));
print_r(json_decode($result));
?>
```
{% elif item.request.method == "GET" %}

{% if resp.python_client_example %}
``` python--PyClient
{{ resp.python_client_example }}
```
{% endif %}
``` python--Python
api.get("{{ resp.request.url.path }}").json()
```
``` javascript
api.get("{{ resp.request.url.path }}", (resp) => {})
```
``` php
<?php
$result = $api->get("{{ resp.request.url.path }}");
print_r(json_decode($result));
?>
```
``` shell
{% if 'user' not in resp.request.url.path %}
curl https://api.qtrade.io{{ resp.request.url.path }}
{% endif %}
```
{% endif %}

> {{ resp.code }} Response 

``` json
{{ resp.body | to_pretty_json }}
```
{% endfor %}

{{ item.request.description }}

{% if item.request.body and item.request.body.params %}

### POST Body

Variable | Example | Description
--------- | ------ | -----------
{% for dict in item.request.body.params %}
{{dict.key}} | {{dict.value}} | {{dict.description}}
{% endfor %}
{% endif %}

{% if item.request.url.variable %}

### Path variables

Variable | Description
--------- | -----------
{% for prop in item.request.url.variable %}
{{ prop.key }} | {{ prop.description }}
{% endfor %}
{% endif %}

{% if item.request.url.query %}

### Query params

Parameter | Type | Description
--------- | ---- | -----------
{% for prop in item.request.url.query %}
{{ prop.key }} | {{ prop.value }} | {{ prop.description }}
{% endfor %}
{% endif %}

`{{ item.request.method }} {{ item.request.url.path }}`

{% endmacro %}

# Public

{% for item in public %}
{{ endpoint(item) }}
{% endfor %}

# Private

{% for item in private %}
{{ endpoint(item) }}
{% endfor %}

# Rate Limits

``` json
{
	"X-Ratelimit-Limit": "60",
	"X-Ratelimit-Reset": "56",
	"X-Ratelimit-Remaining": "59",
    ...
}
```

A good rule of thumb is to limit your requests to 1 / second. The rate limit is enforced by limiting the number of requests in a specific time period. The limit is reset after that time period has elapsed. This means your rate limit within that time period is burstable, and not strictly limited to 1/second. You can monitor the current rate limit status by checking the response headers of your requests. Outlined below are the headers we return and how they work.

If you'd like a higher rate limit please contact support and explain your use case.

Header | How it is used
--- | ---
X-Ratelimit-Limit | The number of maximum requests available in the time period
X-RateLimit-Reset | How many seconds until your rate limit resets
X-Ratelimit-Remaining | How many requests you have left for the time period


# CORS

For increased user security we've limited valid CORS origins for private API routes, and some public API routes. Only the qtrade.io domain origin is valid for those API requests, and this means private API requests performed in a browser (ie, via javascript) will fail.

If your app needs private API access we recommend performing your API requests on the server side. For example, if you want to display your qTrade deposit address to someone visiting your website, make the request to the deposit endpoint on the server and return that data to your client in your HTTP response.

Open CORS Endpoint | URL
--- | ---
Currencies | `/currencies`, `/currency/:CODE`
Tickers | `/tickers`, `/ticker/:market_string`
Markets | `/markets`, `/market/:market_string`
Market Orderbook | `/orderbook/:market_string`
Market Trades | `/market/:market_string/trades`

# Postman Collection

For convenience you can download a Postman collection to play around with the API. 

 - Import the collection
 - Import the Environment
 - Set the `hmac_key` and `hmac_key_id` environment variables to match an API key you generated
 - Execute API calls!

### Get the <a href="postman.json">Collection</a> and <a href="postman_environment.json">Environment</a>
