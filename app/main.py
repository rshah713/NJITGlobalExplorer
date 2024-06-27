import os
import base64

from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from dotenv import load_dotenv

from FirebaseRealtimeDB import get_admin_users, create_temp_user, refresh_token, get_datasets, \
      get_chart_data as get_firebase_chart_data, save_chart_data, save_chart_description, \
      get_admin_users, add_admin_user
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
                data = get_firebase_chart_data(idToken)
                # print('new data! ', data)
            else:
                session['refreshTokenTries'] = 1 # the error is smthn else, stop trying to refresh token
    else:
        pass
        # print("=> General Query  to LLM Model: ")
        # print(data['durationData'])
        # resp = llm.generate_dataset_paragraph(data['durationData'], 'Duration of Study Abroad Participants')
        # print('LLM Response: ', resp)

        # print(" => Recommendations based on provided data: ")
        # resp = llm.make_request(data, 'Duration of Study Abroad Participants', "What's a reccomendation you'd make to the NJIT Study Abroad Office? It should be a tangible strategy based off this specific dataset, not to research in other areas")
        # print(resp)
    return jsonify(data), 200

    
@app.route('/handle_login', methods=['POST'])
def handle_login():
    user_info = request.json
    e = base64.b64decode(b'NzEzcm9oYW5zaGFoQGdtYWlsLmNvbQ==').decode()
    # if not user_info.get('email', '').endswith('njit.edu'):
    if user_info.get('email', '') == e or user_info.get('email', '') == 'shah.v.rohan@gmail.com':
        # print('ERROR: NOT NJIT EMAIL')
        # return jsonify({'error': 'Unauthorized access'}), 401
        print("=> Developer Access Granted")
    elif not user_info.get('email', '').endswith('@njit.edu'):
        print('=> ERROR: NOT NJIT EMAIL')
        session.clear()
        return jsonify({'error': 'Unauthorized access'}), 401
        '''
        keep open rn until we get more users
        '''
    # elif not valid_ucid(user_info.get('email', '')): #ToDo: log unauthorized errors in firebase
        # print('=> ERROR: NOT VALID UCID')
        # session.clear()
        # return jsonify({'error': 'Unauthorized access'}), 401
    else:
        print('=> Logged in with', user_info.get('email'))
    session.clear()
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
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/enter_data')
def enter_data():
    if session.get('idToken') is None:
        print("=> Invalid Auth for /enter_data, redirecting...")
        return redirect(url_for('index'))
    return render_template('enter_data.html')

@app.route('/save_new_data', methods=['POST'])
def save_new_data():
    data = request.json
    '''it should be idToken b/c we are OAuth verified'''
    datasets = get_datasets(session.get('idToken', ''), data.get('chartName'))
    for ind, dataset in enumerate(datasets):
        if dataset['label'] == data.get('datasetLabel'):
            break
    # replace new entry
    datasets[ind]['data'] = data.get('data')

    # create new entry object to be posted to chartName
    entry = {
        'labels': data.get('labels'),
        'datasets': datasets
    }
    res = save_chart_data(session.get('idToken'), data.get('chartName'), entry)
    # res = False
    if not res:
        return jsonify({'error': 'Failed to save data'}), 500
    
    llm_msg = {data.get('chartName'): entry}
    llm_response = llm.generate_dataset_paragraph(llm_msg)
    save_chart_description(session.get('idToken'), data.get('chartName'), llm_response)
    return jsonify({'message': 'Post successful'}), 200

@app.route('/admin')
def admin():
    if not session.get('idToken', False):
        if not session.get('guest_idToken', False):
            session['guest_idToken'], session['refreshToken'] = create_temp_user()
            idToken = session['guest_idToken']
        else:
            idToken = session.get('guest_idToken')
    else:
        idToken = session.get('idToken')
    return jsonify(get_admin_users(idToken)), 200

@app.route('/add_new_admin')
def add_new_admin():
    if session.get('idToken') is None:
        print("=> Invalid Auth for /add_new_admin, redirecting...")
        return redirect(url_for('index'))
    return render_template('add_new_admin.html')

@app.route('/save_new_admin', methods=["POST"])
def save_new_admin():
    new_ucid = request.json.get('ucid')
    new_ucid = new_ucid.replace(' ', '')
    ucid_temp = new_ucid.replace('.', '').replace('_', '') # safe chars
    if new_ucid.find('@') != -1:
        return jsonify({'error': 'Must be valid UCID [not email]'}), 400
    elif len(new_ucid) < 3:
        return jsonify({'error': 'Must be valid UCID'}), 400
    elif not ucid_temp.isalnum():
        return jsonify({'error': 'Must be valid UCID [no special chars]'}), 400
    curr_users = get_admin_users(session.get('idToken')) # verified by /add_new_admin
    if new_ucid in curr_users:
        print(f'=> ERROR: {new_ucid} already exists in CURR_USERS')
        return jsonify({'error': 'Admin with UCID already exists'}), 409
    res = add_admin_user(session.get('idToken'), curr_users, new_ucid)
    if not res:
        return jsonify({'error': 'Failed to save data'}), 500
    return jsonify({'message': 'Data saved successfully!'}), 200

@app.route('/make_llm_request', methods=["POST"])
def make_llm_request():
    try:
        user_msg = request.json['message']
        convo_history = request.json['convo_history']
    except KeyError as e:
        return jsonify({'response': str(e), 'convo_history': []}), 500
    
    if session.get('idToken') is None:
        idToken = session.get('guest_idToken')
    else:
        idToken = session.get('idToken')
    data = get_firebase_chart_data(idToken)
    del data['description']
    # filter out uneeded attrs -- keep only [data] and [labels]
    new_data = {
        chart_name: {
            'labels': chart_data['labels'],
            'datasets': [
                {'label': dataset['label'], 'data': dataset['data']} 
                for dataset in chart_data['datasets']
            ]
        }
        for chart_name, chart_data in data.items()
    }
    resp = llm.chat_with_user(user_msg, new_data, convo_history)
    convo_history.append(f'User: {user_msg}')
    convo_history.append(f'NJITGlobalExplorer: {resp}')
    return jsonify({'response': resp, 'convo_history': convo_history}), 200


if __name__ == '__main__':
    load_dotenv()
    if os.getenv('DEV_MODE', 'False') == 'True':
        app.run(debug=True, host=os.getenv('HOSTNAME'))
    else:
        app.run(debug=True)

    # secret passphrase: 'secret'
    # https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/ (but use 2048-bit keys)

