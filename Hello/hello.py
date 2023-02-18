import json
import jwt
import time

from hyper import HTTPConnection

ALGORITHM = 'ES256'
APNS_KEY_ID = 'U4RR5Q393V'
APNS_AUTH_KEY = 'AuthKey_U4RR5Q393V.p8'
TEAM_ID = 'LN49985R3R'
BUNDLE_ID = 'com.evorait.ionictest'

REGISTRATION_ID = 'BA5EEB210D0964A822708108CEF3A51810F9ADEDE563A9058EF5EF3851D8B3D3'

f = open(APNS_AUTH_KEY)
secret = f.read()

token = jwt.encode(
    {
        'iss': TEAM_ID,
        'iat': time.time()
    },
    secret,
    algorithm=ALGORITHM,
    headers={
        'alg': ALGORITHM,
        'kid': APNS_KEY_ID
    }
)

path = '/3/device/{0}'.format(REGISTRATION_ID)

request_headers = {
    'apns-expiration': '0',
    'apns-priority': '10',
    'apns-topic': BUNDLE_ID,
    'authorization': 'bearer {0}'.format(token.decode('ascii'))
}

#Open a connection to APNS server
conn = HTTPConnection('api.development.push.apple.com:443')

payload_data = {"aps":{"alert":"Testing.. (0)","badge":1,"sound":"default"}}

payload = json.dumps(payload_data).encode('utf-8')

#Send the request
conn.request(
    'POST',
    path,
    payload,
    headers=request_headers
)
resp = conn.get_response()
print(resp.status)
print(resp.read())

#If we are sending multiple request then use same connection
payload_data = {"aps":{"alert":"Testing.. (1)","badge":1,"sound":"default"}}

payload = json.dumps(payload_data).encode('utf-8')

#Send the request
conn.request(
    'POST',
    path,
    payload,
    headers=request_headers
)
resp = conn.get_response()
print(resp.status)
print(resp.read())

#https://gobiko.com/blog/token-based-authentication-http2-example-apns/