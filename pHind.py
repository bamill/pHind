#!/usr/bin/python3
import sys
from sys import argv
import requests
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

prompt_mode = False
if len(argv) > 1:
    file = argv[1]
    lines = [line.rstrip('\n') for line in open(file, 'r')]
else:
    prompt_mode = True

def user_locs(user):
    return '/v2/users/' + user + '/locations'

def check_vars():
    var_l = ['PHIND_U', 'PHIND_S']
    for v in var_l:
        if v not in os.environ:
            print('env vars not correct')
            sys.exit()

check_vars()
client_id = os.environ['PHIND_U']
client_secret = os.environ['PHIND_S']
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

base_url = 'https://api.intra.42.fr'

token = oauth.fetch_token(
    'https://api.intra.42.fr/oauth/token',
    client_id=client_id,
    client_secret=client_secret)

def prompt():
    r = oauth.get(base_url + user_locs(input('user to find: ')), params={'filter[active]': 'true'})
    assert r.status_code is 200, 'Unexpected status {}'.format(r.status_code)
    ret = r.json()
    if ret != []:
        print(ret[0]['host'])
    else:
        print('Unavailable')

if prompt_mode is True:
    prompt()
    while True:
        response = input("Find another user? Y/N \n")
        if response not in ['Y', 'y', 'Yes', 'yes']:
            break
        prompt()
else:
    for line in lines:
        r = oauth.get(base_url + user_locs(line))
        assert r.status_code is 200, 'Unexpected status {}'.format(r.status_code)
        ret = r.json()
        if ret != []:
            print(ret[0]['host'])
        else:
            print('Unavailable')
