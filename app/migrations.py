'''
Script to create Firebase RTDB images to store as backups
Avoids paying for Firebase Blaze plan

Rohan Shah
6/21/24
'''

import os
import json
from datetime import datetime
import urllib.parse as parse
import urllib.error as error
import urllib.request as request


from dotenv import load_dotenv


def main():
    FIREBASE_URL = os.getenv('FIREBASE_URL')
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
    FIREBASE_BACKUP_URL = os.getenv('FIREBASE_BACKUP_URL')
    FIREBASE_BACKUP_API_KEY = os.getenv('FIREBASE_BACKUP_API_KEY')
    FIREBASE_BACKUP_EMAIL = os.getenv('FIREBASE_BACKUP_EMAIL')
    FIREBASE_BACKUP_PASSWORD = os.getenv('FIREBASE_BACKUP_PASSWORD')

    #############################
    # Authenticate Main Project #
    #############################
    ENDPOINT = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}'
    payload = {
        'returnSecureToken': True
    }
    payload = json.dumps(payload).encode()
    HEADERS = {"content-type": "application/json; charset=UTF-8" }
    req = request.Request(ENDPOINT, data=payload, headers=HEADERS, method="POST")
    try:
        resp = request.urlopen(req)
        resp = resp.read().decode('utf-8')
        resp = json.loads(resp)
        guest_token = resp['idToken']
    except error.HTTPError as e:
        print(f"Error: {e} to {ENDPOINT}")
        guest_token = None

    auth = {'auth': guest_token}
    auth = parse.urlencode(auth)

    #############################
    #   Snapshot Current Data   #
    #############################
    ENDPOINT = FIREBASE_URL + '.json?' + auth
    try:
        resp = request.urlopen(ENDPOINT)
        resp = resp.read().decode('utf-8')
        image = json.loads(resp)
    except error.HTTPError as e:
        print(f"Error: {e} to {ENDPOINT}")
        image = False
    
    #############################
    #    Authenticate Backup    #
    #############################
    ENDPOINT_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + FIREBASE_BACKUP_API_KEY
    headers = {"content-type": "application/json; charset=UTF-8" }
    user_payload = {
        'email' : FIREBASE_BACKUP_EMAIL,
        'password' : FIREBASE_BACKUP_PASSWORD,
        'returnSecureToken' : True
    }
    user_payload = json.dumps(user_payload).encode()
    req = request.Request(ENDPOINT_URL, data=user_payload, headers=headers, method="POST")
    try:
        new_user_json = request.urlopen(req)
        new_user_json = new_user_json.read().decode('utf-8')
        new_user_json = json.loads(new_user_json) # json string --> python dict
        idToken = new_user_json['idToken']
    except error.HTTPError as err:
        print(str(err))
        idToken = None

    auth = {'auth': idToken}
    auth = parse.urlencode(auth)

    #############################
    #   Store Image to Backup   #
    #############################
    ENDPOINT = FIREBASE_BACKUP_URL + '.json?' + auth
    curr_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {curr_datetime : image}
    payload = json.dumps(payload).encode()
    req = request.Request(ENDPOINT, data=payload, headers=HEADERS, method="PATCH")
    try:
        resp = request.urlopen(req)
        resp = resp.read().decode('utf-8')
        resp = json.loads(resp)
        # print(resp)
    except error.HTTPError as e:
        print(f"Error: {e} to {ENDPOINT}")
        


if __name__ == "__main__":
    load_dotenv()
    main()