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
    new_user = make_firebase_request(ENDPOINT, payload, method="POST")
    if new_user:
        return new_user.get('idToken')
    print("ERROR: Failed to create anonymous user")
    return False

def add_admin_user(idToken, new_ucid):
    ENDPOINT = get_firebase_db_url() + '.json'
    curr_users = get_admin_users(idToken)
    if not curr_users:
        print(f'ERROR: Could not add {new_ucid} as could not read CURR_USERS from Firebase')
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

def get_chart_data(idToken):
    ENDPOINT = get_firebase_db_url() + 'data.json'
    auth = {'auth': idToken}
    auth = parse.urlencode(auth)
    ENDPOINT += '?' + auth
    return make_firebase_request(ENDPOINT)

# idToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImRmOGIxNTFiY2Q5MGQ1YjMwMjBlNTNhMzYyZTRiMzA3NTYzMzdhNjEiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9uaml0Z2xvYmFsZXhwbG9yZXIiLCJhdWQiOiJuaml0Z2xvYmFsZXhwbG9yZXIiLCJhdXRoX3RpbWUiOjE3MTgyMDIzMjIsInVzZXJfaWQiOiJFclpkM3h0T2E0VWpsVVo3d09KRDU5WmlmQmgxIiwic3ViIjoiRXJaZDN4dE9hNFVqbFVaN3dPSkQ1OVppZkJoMSIsImlhdCI6MTcxODIwMjMyMiwiZXhwIjoxNzE4MjA1OTIyLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7fSwic2lnbl9pbl9wcm92aWRlciI6ImFub255bW91cyJ9fQ.dvYO864Ao_ahvJXqNxBnlZJL4tcuP3lNhouiriaa9maSXLJ1j6855Pe6C3vUDouawZ58KgXAbf_Zu3fJoMIIee8SWuX6SFQ7ExhO40PgudOwuUZHjyTJDSgMr95VZtUUlVZzfy_wBUZVoUJGObBunxpqBr8HOD-zOJKbomLqSMlvVf2xOqbLNjpHjdua7OUqDyvduJ9b84sf7QCLRfjFYLSL129vm03fGhE07k61X3MgM3zrnYQHSE8-W5FVdO9de_HTUBlfjRNyXA-LyV3AS9UJiPjWuLnaBQS2UWz0uj7TG3YsA_AjiWbZpyJ7ezQ9O3a34lvRen2AMEddCIkMXA'
# endpoint = get_firebase_db_url() + 'data.json'
# auth = {'auth': idToken}
# auth = parse.urlencode(auth)
# endpoint += '?' + auth

# payload = {'chart1': [10, 20, 30], 'chart2': [30, 20, 10]}
# make_firebase_request(endpoint, payload)
