import os
import base64

from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from dotenv import load_dotenv

from FirebaseRealtimeDB import get_admin_users, create_temp_user

app = Flask(__name__)
app.secret_key = 'secret_key'

def valid_ucid(email):
    ucid = email.split('@')[0]
    anon_user_token = create_temp_user()
    return ucid in get_admin_users(anon_user_token)

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
    
@app.route('/handle_login', methods=['POST'])
def handle_login():
    user_info = request.json
    e = base64.b64decode(b'NzEzcm9oYW5zaGFoQGdtYWlsLmNvbQ==').decode()
    # if not user_info.get('email', '').endswith('njit.edu'):
    if user_info.get('email', '') == e:
        print('ERROR: NOT NJIT EMAIL')
        return jsonify({'error': 'Unauthorized access'}), 401
    elif not valid_ucid(user_info.get('email', '')): #ToDo: log unauthorized errors in firebase
        print('ERROR: NOT VALID UCID')
        return jsonify({'error': 'Unauthorized access'}), 401
    else:
        print('logged in w/', user_info.get('email'))
    session['is_logged_in'] = True
    session['uid'] = user_info.get('uid')
    session['email'] = user_info.get('email')
    session['displayName'] = user_info.get('displayName')
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

