import os
import base64

from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from dotenv import load_dotenv

from FirebaseRealtimeDB import get_admin_users, create_temp_user, refresh_token, get_chart_data as get_firebase_chart_data
import llm


app = Flask(__name__)
app.secret_key = 'secret_key'

def valid_ucid(email):
    ucid = email.split('@')[0]
    if not session.get('guest_idToken', False): # no guest has been created yet
        print('=> CREATE GUEST idToken')
        session['guest_idToken'], session['refreshToken'] = create_temp_user()
    return ucid in get_admin_users(session['guest_idToken'])

@app.context_processor
def inject_api_key():
    return {'FIREBASE_API_KEY': os.getenv("FIREBASE_API_KEY")}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    if request.method == "GET":
        previous_url = request.args.get('next', '/')
        return render_template('login.html', previous_url=previous_url, api_key=os.getenv("FIREBASE_API_KEY"))
    else:
        return 'POST'
    
@app.route('/get_chart_data', methods=['GET'])
def get_chart_data():
    if not session.get('idToken', False): # we aren't signed in, create a temp user
        session['is_logged_in'] = False
        if not session.get('guest_idToken', False): # no guest has been created yet
            session['guest_idToken'], session['refreshToken'] = create_temp_user()
        idToken = session['guest_idToken']
        print('=> Using GUEST idToken for Charts')
    else:
        idToken = session.get('idToken')
        print('=> Using USER idToken for Charts')
    data = get_firebase_chart_data(idToken)
    if not data: # it could mean idToken expired OR we actually don't have rights
        session['refreshTokenTries'] = 0
        if session.get('refreshTokenTries', 0) == 0:
            new_token = refresh_token(session.get('refreshToken', ''))
            if new_token:
                session['refreshTokenTries'] = 0 # reset back to 0
                if not session.get('idToken', False): # still operating w/ guest account
                    idToken = session['guest_idToken'] = new_token
                else:
                    idToken = session['idToken'] = new_token
                print('new idtok', idToken)
                data = get_firebase_chart_data(idToken)
                print('new data', data)
            else:
                session['refreshTokenTries'] = 1 # the error is smthn else, stop trying to refresh token
    else:
        print("=> Sending data to LLM Model w/ query: ")
        resp = llm.make_request(data, 'Duration of Study Abroad Participants', 'What year has an abormally low % of Semester Abroad students?')
        print(resp)
    return jsonify(data), 200

    
@app.route('/handle_login', methods=['POST'])
def handle_login():
    user_info = request.json
    e = base64.b64decode(b'NzEzcm9oYW5zaGFoQGdtYWlsLmNvbQ==').decode()
    # if not user_info.get('email', '').endswith('njit.edu'):
    if user_info.get('email', '') == e:
        print('ERROR: NOT NJIT EMAIL')
        return jsonify({'error': 'Unauthorized access'}), 401
    # elif not valid_ucid(user_info.get('email', '')): #ToDo: log unauthorized errors in firebase
    #     print('ERROR: NOT VALID UCID')
    #     return jsonify({'error': 'Unauthorized access'}), 401
    else:
        print('=> Logged in with', user_info.get('email'))
    print('=> GET valid_ucids: ', valid_ucid(user_info.get('email', '')))
    session['is_logged_in'] = True
    session['uid'] = user_info.get('uid')
    session['email'] = user_info.get('email')
    session['displayName'] = user_info.get('displayName')
    session['idToken'] = user_info.get('idToken')
    session['refreshToken'] = user_info.get('refreshToken')
    return jsonify({'message': 'Login successful'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    session['is_logged_in'] = False
    # return redirect(url_for('index'))  # Redirect to the homepage or login page
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
    # secret passphrase: 'secret'
    # https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/ (but use 2048-bit keys)

