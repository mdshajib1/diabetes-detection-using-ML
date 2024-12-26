import pickle
from flask import Flask, request, jsonify, url_for, render_template, redirect, session

import numpy as np
import pandas as pd

app = Flask(__name__, static_folder='static')
app.secret_key = 'supersecretkey'  # Needed for session management

# Load the model
classifier = pickle.load(open('classifier.pkl', 'rb'))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    # Simple authentication check
    if username == 'Pythonic Pair' and password == '010535':
        session['logged_in'] = True
        return redirect(url_for('home'))
    else:
        error = 'Invalid Credentials. Please try again.'
        return render_template('login.html', error=error)

@app.route('/home')
def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/tips')
def tips():
    if 'logged_in' in session and session['logged_in']:
        return render_template('tips.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/about')
def about():
    if 'logged_in' in session and session['logged_in']:
        return render_template('about.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/predict_api', methods=['POST'])
def predict_api():
    if 'logged_in' in session and session['logged_in']:
        data = request.json['data']
        data = np.array(data).reshape(1, -1)
        output = classifier.predict(data)[0]
        if output == 1:
            result = "The result is 1. You might have diabetes."
        else:
            result = "The result is 0. You might not have diabetes."
        return jsonify(result)
    else:
        return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'logged_in' in session and session['logged_in']:
        data = [float(x) for x in request.form.values()]
        data = np.array(data).reshape(1, -1)
        output = classifier.predict(data)[0]
        result = "The result is 1. You might have diabetes." if output == 1 else "The result is 0. You might not have diabetes."
        return render_template("home.html", prediction_text=result)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
