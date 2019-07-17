use GuzzleHttp\Client;

$client = new Client([
    'base_uri' => 'http://127.0.0.1:8000/api/v1/message/1/',
    'timeout'  => 2.0,
]);
