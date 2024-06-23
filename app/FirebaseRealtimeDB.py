import urllib.request as request
import urllib.parse as parse
import urllib.error as error
import os
import json
'''
data
    |
    | - chart1
    | - chart2
    | - chart3

users [valid UCIDs who can access data entry page]
    |
    | - user1
    | - user2
    | - user3
'''
from dotenv import load_dotenv
load_dotenv()

def get_firebase_api_key():
    return os.getenv('FIREBASE_API_KEY')

def get_firebase_db_url():
    return os.getenv('FIREBASE_URL')

def make_firebase_request(endpoint, payload=None, method="PATCH", idToken=''):
    if idToken != '':
        auth = {'auth': idToken}
        auth = parse.urlencode(auth)
        endpoint += '?' + auth
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
        print(f"Error: {e} to {endpoint}")
        return False

def create_temp_user():
    ENDPOINT = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={get_firebase_api_key()}'
    payload = {
        'returnSecureToken': True
    }
    new_user = make_firebase_request(ENDPOINT, payload, method="POST")
    if new_user:
        return new_user.get('idToken'), new_user.get('refreshToken')
    print("ERROR: Failed to create anonymous user")
    return False

def refresh_token(refreshToken):
    print('refreshing w/', refreshToken)
    ENDPOINT = f"https://securetoken.googleapis.com/v1/token?key={get_firebase_api_key()}"
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refreshToken
    }
    new_user = make_firebase_request(ENDPOINT, payload, method="POST")
    if new_user:
        return new_user.get('id_token')
    print("ERROR: Failed to refreshToken")
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
    return make_firebase_request(ENDPOINT, payload, idToken=idToken)

def get_admin_users(idToken):
    ENDPOINT = get_firebase_db_url() + 'users.json'
    return make_firebase_request(ENDPOINT, idToken=idToken)

def get_chart_data(idToken):
    ENDPOINT = get_firebase_db_url() + 'data.json'
    return make_firebase_request(ENDPOINT, idToken=idToken)

def save_chart_data(idToken, chartName, data):
    ENDPOINT = get_firebase_db_url() + 'data.json'
    payload = {chartName: data}
    return make_firebase_request(ENDPOINT, payload, idToken=idToken)

def save_chart_description(idToken, chartName, desc):
    ENDPOINT = get_firebase_db_url() + 'data/description.json'
    payload = {chartName: desc}
    return make_firebase_request(ENDPOINT, payload, idToken=idToken)

def get_datasets(idToken, chartName):
    url = f'data/{chartName}.json'
    ENDPOINT = get_firebase_db_url() + url
    return make_firebase_request(ENDPOINT, idToken=idToken).get('datasets')

# idToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImRmOGIxNTFiY2Q5MGQ1YjMwMjBlNTNhMzYyZTRiMzA3NTYzMzdhNjEiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9uaml0Z2xvYmFsZXhwbG9yZXIiLCJhdWQiOiJuaml0Z2xvYmFsZXhwbG9yZXIiLCJhdXRoX3RpbWUiOjE3MTgyMDIzMjIsInVzZXJfaWQiOiJFclpkM3h0T2E0VWpsVVo3d09KRDU5WmlmQmgxIiwic3ViIjoiRXJaZDN4dE9hNFVqbFVaN3dPSkQ1OVppZkJoMSIsImlhdCI6MTcxODIwMjMyMiwiZXhwIjoxNzE4MjA1OTIyLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7fSwic2lnbl9pbl9wcm92aWRlciI6ImFub255bW91cyJ9fQ.dvYO864Ao_ahvJXqNxBnlZJL4tcuP3lNhouiriaa9maSXLJ1j6855Pe6C3vUDouawZ58KgXAbf_Zu3fJoMIIee8SWuX6SFQ7ExhO40PgudOwuUZHjyTJDSgMr95VZtUUlVZzfy_wBUZVoUJGObBunxpqBr8HOD-zOJKbomLqSMlvVf2xOqbLNjpHjdua7OUqDyvduJ9b84sf7QCLRfjFYLSL129vm03fGhE07k61X3MgM3zrnYQHSE8-W5FVdO9de_HTUBlfjRNyXA-LyV3AS9UJiPjWuLnaBQS2UWz0uj7TG3YsA_AjiWbZpyJ7ezQ9O3a34lvRen2AMEddCIkMXA'
# endpoint = get_firebase_db_url() + 'data.json'
# auth = {'auth': idToken}
# auth = parse.urlencode(auth)
# endpoint += '?' + auth

# payload = {'chart1': [10, 20, 30], 'chart2': [30, 20, 10]}
# make_firebase_request(endpoint, payload)

# idToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImRmOGIxNTFiY2Q5MGQ1YjMwMjBlNTNhMzYyZTRiMzA3NTYzMzdhNjEiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9uaml0Z2xvYmFsZXhwbG9yZXIiLCJhdWQiOiJuaml0Z2xvYmFsZXhwbG9yZXIiLCJhdXRoX3RpbWUiOjE3MTgyMTkxOTIsInVzZXJfaWQiOiI3a3RGQ1ZJN0I2aFRIVmJHNkNBeWo5SzFsazkzIiwic3ViIjoiN2t0RkNWSTdCNmhUSFZiRzZDQXlqOUsxbGs5MyIsImlhdCI6MTcxODIxOTE5MiwiZXhwIjoxNzE4MjIyNzkyLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7fSwic2lnbl9pbl9wcm92aWRlciI6ImFub255bW91cyJ9fQ.cshii3FAkEveb8it6E26hmt2pDQ3SCf6ccyDcIYZlsz1Oh4FSTs4NhKAiH7IEsDrxBFR4UuJOayBR0fN6XjnkJOPN5KHPyxm0I_AhCxreNc_HOJGA-TkMFBbXil9S17efdjBELJhQe9gEUnX8BXTE2wpkLtq5XP80ZWBEze6y13LNTCWQBix8XocpQqZd2A1bXHqy2DNO7WRCZR12VPT8I67I-68x6o2bN_TqfD6XOku0Bl0Tm--4C7_u5tHV8CgGX98EyKUaCzSD3AasXSWLRNURE63h6ouHKYPgLekd5CJT8_NDgLqHRKWyDiQjTGEc4_EzqkT6FcElrfIQbDAHg'

# idToken, refreshToken = create_temp_user()


if __name__ == "__main__":
    data = {
                'labels': ['Helped develop job-related skills',
                           'Directly led to first job placement',
                           'Got into desired graduate school'],
                'datasets': [
                    {
                        'label': 'National',
                        'data': [79, 50, 90],
                        'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                        'borderColor': 'rgba(255, 159, 64, 1)',
                        'borderWidth': 1
                    },
                    {
                        'label': 'NJIT',
                        'data': [38, 93, 63],
                        'backgroundColor': 'rgba(255, 255, 0, 0.2)',
                        'borderColor': 'rgba(255, 255, 0, 1)',
                        'borderWidth': 1
                    }
                ]
            }
    idToken = create_temp_user()[0]
    save_chart_data(idToken, 'professional', data)
    # c = get_chart_data(idToken)['abroadParticipation']['datasets'][1]
    # c['spanGaps'] = True
    # l = [1.01]*51
    # c['data'] = l
    # print(c)
    # ENDPOINT = get_firebase_db_url() + 'data/abroadParticipation/datasets/1.json' + f'?auth={idToken}'
    # payload = json.dumps(c).encode()
    # HEADERS = {"content-type": "application/json; charset=UTF-8" }
    # req = request.Request(ENDPOINT, data=payload, headers=HEADERS, method="PATCH")
    # resp = request.urlopen(req)
    # resp = resp.read().decode('utf-8')
    # resp = json.loads(resp)
    # print(resp)
