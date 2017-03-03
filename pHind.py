#!/usr/bin/python3
import sys
from sys import argv
import requests
import os
import re
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def user_locs(user):
    return '/v2/users/' + user + '/locations'

def check_vars():
    var_l = ['PHIND_U', 'PHIND_S']
    for v in var_l:
        if v not in os.environ:
            print('env vars not correct')
            sys.exit()

def user_lookup(user):
    r = oauth.get(base_url + user_locs(user), params={'filter[active]': 'true'})
    if r.status_code == 404:
        print('\x1b[31;1m' + 'User ' + user + ' Not found' + '\x1b[0m')
    else:
        try:
            assert r.status_code is 200, 'Unexpected status {}'.format(r.status_code)
        except AssertionError:
            print('\x1b[31;1m' + 'Bad status return code: ' + str(r.status_code) + '\x1b[0m')
        else:
            ret = r.json()
            if ret != []:
                s = re.split('([a-z][0-9]{1,3})', ret[0]['host'])
                print('\x1b[32;1m' + s[1] + '\x1b[33;1m' + s[3] + '\x1b[34;1m' +
                      s[5] + '\x1b[35;1m' + s[7] + '\x1b[0m')
            else:
                print('\x1b[31;1m' + 'Unavailable' + '\x1b[0m')

def prompt():
    user = input('user to find: ')
    user_lookup(user)

def main():
    prompt_mode = False
    if len(argv) > 1:
        file = argv[1]
        lines = [line.rstrip('\n') for line in open(file, 'r')]
    else:
        prompt_mode = True

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

    if prompt_mode is True:
        prompt()
        while True:
            response = input("Find another user? Y/N \n")
            if response not in ['Y', 'y', 'Yes', 'yes']:
                break
            prompt()
    else:
        for line in lines:
            user_lookup(line)

main()
