<?php
class QtradeAuth 
{
    public $key_id;
    public $key;
    public $base = "https://api.qtrade.io";

    public function __construct($key)
    {
        $key_pieces = explode(":", $key);
        $this->key_id = $key_pieces[0];
        $this->key = $key_pieces[1];
    }

    public function __call($method, $args)
    {
        $request_path = $args[0];
        $timestamp = time();
        if ($method === "get" || $method === "post") {
            $body = array_key_exists(1, $args) ? $args[1] : '';
        } else {
            throw new BadMethodCallException;
        }

        // Build hmac sig
        $sig_text = strtoupper($method) . "\n";
        $sig_text .= $request_path . "\n";
        $sig_text .= $timestamp . "\n";
        $sig_text .= $body . "\n";
        $sig_text .= $this->key;
        $hmac_sig = base64_encode(hash("sha256", $sig_text, $raw_output = TRUE));

        // Build CURL req
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, strtoupper($method)); 
        curl_setopt($ch, CURLOPT_URL, $this->base . $request_path);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        if ($method === "post") {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        }
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            "Content-Type: application/json; charset=utf-8",
            "Accept: application/json",
            'Authorization: HMAC-SHA256 ' . $this->key_id . ':' . $hmac_sig,
            'HMAC-Timestamp: ' . $timestamp,
        ));
        return curl_exec($ch);
    }
}

$api = new QtradeAuth("1:1111111111111111111111111111111111111111111111111111111111111111");

// GET request
$result = $api->get("/v1/user/me");
print_r(json_decode($result));

// POST request
$req = array(
    "amount"  => "1",
    "price" => "2",
    "market_id" => 7
);
$result = $api->post("/v1/user/buy_limit", json_encode($req));
print_r(json_decode($result));
?>