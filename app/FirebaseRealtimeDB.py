import urllib.request as request
import urllib.parse as parse
import urllib.error as error
import os
import json

from dotenv import load_dotenv
load_dotenv()

def get_firebase_api_key():
    return os.getenv('FIREBASE_API_KEY')

def get_firebase_db_url():
    return os.getenv('FIREBASE_URL')

def make_firebase_request(endpoint, payload=None, method="PATCH"):
    if payload:
        payload = json.dumps(payload).encode()
        HEADERS = {"content-type": "application/json; charset=UTF-8" }
        req = request.Request(endpoint, data=payload, headers=HEADERS, method=method)
    else:
        req = endpoint
    
    try:
        resp = request.urlopen(req)
        resp = resp.read().decode('utf-8')
        resp = json.loads(resp)
        return resp
    except error.HTTPError as e:
        print(f"Error: {e}")
        return False

def create_temp_user():
    ENDPOINT = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={get_firebase_api_key()}'
    payload = {
        'returnSecureToken': True
    }
    print(ENDPOINT)
    new_user = make_firebase_request(ENDPOINT, payload, method="POST")
    if new_user:
        return new_user.get('idToken')
    print("ERROR: Failed to create anonymous user")
    return False

def add_admin_user(idToken, new_ucid):
    ENDPOINT = get_firebase_db_url() + '.json'
    curr_users = get_admin_users(idToken)
    if curr_users is None:
        print(f'ERROR: Could not {new_ucid} as could not read CURR_USERS from Firebase')
        return False
    elif new_ucid in curr_users:
        print(f'ERROR: {new_ucid} already exists in CURR_USERS')
        return True
    curr_users.append(new_ucid)
    payload = {'users': curr_users}
    auth = {'auth': idToken}
    auth = parse.urlencode(auth)
    ENDPOINT += '?' + auth
    return make_firebase_request(ENDPOINT, payload)

def get_admin_users(idToken):
    ENDPOINT = get_firebase_db_url() + 'users.json'
    auth = {'auth': idToken}
    auth = parse.urlencode(auth)
    ENDPOINT += '?' + auth
    return make_firebase_request(ENDPOINT)

