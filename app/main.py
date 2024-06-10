from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = 'secret_key'

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
    app.run(debug=True)

