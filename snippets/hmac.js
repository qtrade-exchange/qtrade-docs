var crypto = require('crypto');
var https = require('https');

class QtradeAuth {
  constructor(key) {
    [this.keyID, this.key] = key.split(":");
    this.host = 'api.qtrade.io';
  }
  req(method, endpoint, body='', handleData) {
    let timestamp = Math.floor(Date.now() / 1000);

    // Create hmac sig
    let sig_text = method + "\n";
    sig_text += endpoint + "\n";
    sig_text += timestamp + "\n";
    sig_text += body + "\n";
    sig_text += this.key;
    var hash = crypto.createHash('sha256').update(sig_text, 'utf8').digest().toString('base64');

    var opt = {
      host: this.host,
      path: endpoint,
      method: method,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'HMAC-SHA256 ' + this.keyID + ':' + hash,
        "HMAC-Timestamp": timestamp,
      }
    };

    var output = '';
    let req = https.request(opt, (res) => {
      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        output += chunk;
      });
      res.on('end', () => {
        handleData(JSON.parse(output));
      })
    });
    req.write(body);
    req.end();
  }
  get(endpoint, handleData) {
    return this.req("GET", endpoint, undefined, handleData);
  }
  post(endpoint, body, handleData) {
    return this.req("POST", endpoint, body, handleData);
  }
}

let api = new QtradeAuth("1:1111111111111111111111111111111111111111111111111111111111111111");

// GET request
api.get("/v1/user/me", (resp) => {
  console.log(resp);
});

// POST request
payload = {
  "amount": "1",
  "price": "0.01",
  "market_id": 1,
};
api.post("/v1/user/sell_limit", JSON.stringify(payload), (resp) => {
  console.log(resp);
});


// Generated headers are:
{
  data: {
    user: {
      id: 1111111,
      email: 'hugh@example.com',
      lname: 'Jass',
      fname: 'Hugh',
      verified_email: true,
      tfa_enabled: false,
      withdraw_limit: 0,
      verification: 'none',
      can_withdraw: true,
      can_login: true,
      can_trade: true,
      referral_code: '6W56QFFVIIJ2',
      email_addresses: [Array]
    }
  }
}


// Generated body is:
{
  data: {
    order: {
      id: 8932314,
      market_amount: '1',
      market_amount_remaining: '1',
      created_at: '2018-13-12T23:18:01.070552Z',
      price: '0.01',
      order_type: 'sell_limit',
      market_id: 1,
      open: true,
      trades: []
    }
  }
}
