---
title: qTrade API Docs

language_tabs: # must be one of https://git.io/vQNgJ
  - python

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


# Authentication

qTrade offers JWT and HMAC authentication methods. All requests and responses are the `application/json` content type return typical HTTP status codes.

This documentation will only cover HMAC authentication protocols.


## HMAC authentication with an API key


``` python
{{ load_snippet('hmac.py') }}
```

The HMAC protocol uses an API key issued on the user settings page. API keys have a limited set of permissions and you should always issue a key with the minimum set of permissions needed. API keys may be revoked on the settings page

API Key permissions are mapped into `realms` and each `realm` is granted access to specific API endpoints

Realm | Endpoints 
--- | --- 
Info | `/user/balances`, `/user/withdraws`, `/user/deposits`, `/user/orders`
Withdraw | `/user/withdraw`
Deposit | `/user/deposit_address/{currency_code}` 
Trade | `/user/sell_limit`, `/user/buy_limit`, `/user/cancel_order`


## Rate Limits

A good rule of thumb is to limit your requests to 1 / second. The rate limit is enforced by limiting the number of requests in a specific time period. The limit is reset after that time period has elapsed. This means your rate limit within that time period is burstable, and not strictly limited to 1/second. You can monitor the current rate limit status by checking the response headers of your requests. Outlined below are the headers we return and how they work.

If you'd like a higher rate limit please contact support and explain your use case.

Header | How it is used
--- | ---
X-Ratelimit | The number of maximum requests available in the time period
X-RateLimit-Reset | How many seconds until your rate limit resets
X-Ratelimit-Remaining | How many requests you have left for the time period


## CORS

<aside class="warning">
  Public API currently restricts CORS origins. This is planned to be removed
</aside>

For increased user security we've limited valid CORS origins for private API routes. Only the qtrade.io domain origin is valid for private API requests, and this means private API requests performed in a browser (ie, via javascript) will fail.

If your app needs private API access we recommend performing your API requests on the server side. For example, if you want to display your qTrade deposit address to someone visiting your website, make the request to the deposit endpoint on the server and return that data to your client in your HTTP response.

Endpoint | Access-Control-Allow-Origin
--- | ---
Public endpoints | *
Private endpoints | https://qtrade.io


{% macro endpoint(item) %}
## {{ item.name }}



{% for resp in item.response %}

{% if item.request.method == "POST" and resp.originalRequest.body.raw %}

``` python
req = {{ resp.originalRequest.body.raw | json_to_python_dict }}
api.post("/{{ item.request.url.path | join("/") }}", json=req).json()
```
{% elif item.request.method == "GET" %}

``` python
api.get("/{{ item.request.url.path | join("/") }}").json()
```
{% endif %}

> {{ resp.code }} Response 

``` json
{{ resp.body | to_pretty_json }}
```
{% endfor %}

{{ item.request.description }}

{% if item.request.url.variable %}
Parameter | Type | Description
--------- | ---- | -----------
{% for prop in item.request.url.variable %}
{{ prop.key }} | {{ prop.value }} | {{ prop.description }}
{% endfor %}
{% endif %}

{% if item.request.url.query %}
Parameter | Type | Description
--------- | ---- | -----------
{% for prop in item.request.url.query %}
{{ prop.key }} | {{ prop.value }} | {{ prop.description }}
{% endfor %}
{% endif %}

{% if item.extra.properties %}
Parameter | Type | Description
--------- | ---- | -----------
{% for key, val in item.extra.properties.items() %}
{{ key }} | {{ val.type }} | {{ val.description }}
{% endfor %}
{% endif %}

`{{ item.request.method }} {{ item.request.url.raw | apply_env }}`

{% endmacro %}

# Public

{% for item in public %}
{{ endpoint(item) }}
{% endfor %}

# Private

{% for item in private %}
{{ endpoint(item) }}
{% endfor %}

# Postman Collection

For convenience, you can download a Postman collection to play around with the API.

<a href="postman.json">Download Here</a>
