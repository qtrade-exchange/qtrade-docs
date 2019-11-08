# Errors

<blockquote><br>
<p>Response 403 </p>
</blockquote>

``` json
{
    "errors": [
        {
            "code": "invalid_auth",
            "title": "Invalid HMAC signature"
        }
    ]
}
```
Errors return with a JSON object explaining the cause, if applicable.

The qTrade API returns the following error codes:


Error Code | Meaning
---------- | -------
400 | Bad Request -- Your request is invalid. Typically bad JSON or missing values.
401 | Unauthorized -- Your API key didn't validate.
403 | Forbidden -- Your API key doesn't have permission to do that.
404 | Not Found -- The specified item (market, order, api key, etc) was not found.
429 | Too Many Requests -- You're making API calls too rapidly, slow down!
500 | Internal Server Error -- We had a problem with our server. Try again later.
503 | Service Unavailable -- We're temporarily offline for maintenance. Please try again later.
