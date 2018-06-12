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

Welcome to the qTrade API documentation. These documents detail how to use qTrade's exchange API and are open source [on github](https://github.com/icook/qtrade-docs). If you'd like to make a correction or suggest any changes please feel free to make a pull request.

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

{% if item.request.method == "POST" and resp.originalRequest.body.raw %}
> Request

``` json
{{ resp.originalRequest.body.raw | to_pretty_json }}
```
{% endif %}

> {{ resp.code }} Response 

``` json
{{ resp.body | to_pretty_json }}
```
{% endfor %}

{{ item.request.description }}

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
