---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - python
  - shell

toc_footers:
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true
---

# Authentication

> To use JWT authentication

``` python
{{ load_snippet('password.py') }}
```

``` shell
export TOKEN=$(curl -H -q "Content-Type: application/json" \
                    -X POST \
                    -d '{"email":"t@test.com","password":"test12345"}' \
                    {{ env.url }}v1/login | jq -r '.data.token')
```

<blockquote class="lang-specific python">
<p>To use HMAC authentication with an API key</p>
</blockquote>

``` python
{{ load_snippet('hmac.py') }}
```


{% macro endpoint(item) %}
## {{ item.name }}

{{ item.request.description }}

{% if item.extra.properties %}
Parameter | Type | Description
--------- | ---- | -----------
{% for key, val in item.extra.properties.items() %}
{{ key }} | {{ val.type }} | {{ val.description }}
{% endfor %}
{% endif %}

`{{ item.request.method }} {{ item.request.url.raw | apply_env }}`

{% for resp in item.response %}

{% if item.request.method == "POST" and resp.originalRequest.body.raw %}
``` shell
curl -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${TOKEN}" \
     -X POST \
     -d '{{ resp.originalRequest.body.raw }}' \
     {{ env.url }}v1/user/me
```

``` python
req = {{ resp.originalRequest.body.raw | json_to_python_dict }}
api.post("/{{ item.request.url.path | join("/") }}", json=req).json()
```
{% elif item.request.method == "GET" %}
``` shell
curl -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${TOKEN}" \
     {{ env.url }}v1/user/me
```

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
