from flask import Flask, redirect, url_for, render_template, request, session
import ssl
import os 

app = Flask(__name__)
app.secret_key = 'secret_key'

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path1 = os.path.join(current_directory, 'server.crt')
file_path2 = os.path.join(current_directory, 'server.key')
context.load_cert_chain(file_path1, file_path2)

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
        return render_template('login.html', previous_url=previous_url)
    else:
        return 'POST'

@app.route('/logout')
def logout():
    session['is_logged_in'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, ssl_context=context)
    # secret passphrase: 'secret'
    # https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/ (but use 2048-bit keys)

