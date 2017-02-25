#!/usr/bin/python3
import sys
from sys import argv
import requests
import os
from requests_oauthlib import OAuth2Session

prompt_mode = False
if len(argv) > 1:
    file = argv[1]
    lines = [line.rstrip('\n') for line in open(file, 'r')]
else:
    prompt_mode = True

def user_locs(user):
    return '/v2/users/' + user + '/locations'
if 'PHIND_U' not in os.environ or 'PHIND_S' not in os.environ:
    print('env vars not correct')
    sys.exit()
client_id = os.environ['PHIND_U']
client_secret = os.environ['PHIND_S']
redirect_uri = 'https://github.com/bamill/pHind'
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
base_url = 'https://api.intra.42.fr'
authorization_url, state = oauth.authorization_url(
    'https://api.intra.42.fr/oauth/authorize?client_id=881c28693b370f4c24a5bb22a88824b7a1081fe8e90ad1e149a6b59e6cfc003f&redirect_uri=https%3A%2F%2Fgithub.com%2Fbamill%2FpHind&response_type=code')

print('Please go to {} and authorize access.'.format(authorization_url))

authorization_response = input('Enter the full callback URL: ')

token = oauth.fetch_token(
    'https://api.intra.42.fr/oauth/token',
    authorization_response=authorization_response,
    client_secret=client_secret)

if prompt_mode is True:
    r = oauth.get(base_url + user_locs(input('user to find: ')), params={'filter[active]': 'true'})
    assert r.status_code is 200, 'Unexpected status {}'.format(r.status_code)
    ret = r.json()
    if ret != []:
        print(ret[0]['host'])
    else:
        print('Unavailable')
else:
    for line in lines:
        r = oauth.get(base_url + user_locs(line))
        assert r.status_code is 200, 'Unexpected status {}'.format(r.status_code)
        ret = r.json()
        if ret != []:
            print(ret[0]['host'])
        else:
            print('Unavailable')
