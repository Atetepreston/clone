# main.py — corrected and ready

from flask import Flask, render_template, request, session, redirect, url_for
from functions import Bank

app = Flask(__name__)
app.secret_key = 'hkjkjhfkjdh1357526%$^"£"'  # For session security

users = {}     # Stores usernames and passwords
user = None    # Global variable to hold the logged-in Bank object

@app.route('/')
def homepage():
    if 'user' in session:
        global user
        user = Bank(session['user'])
        money = user.view_money()
        return render_template('homepage.html', money=money, user=user)
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            user = Bank(username)
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error="Wrong username/password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error="User already exists")
        users[username] = password
        session['user'] = username
        return redirect(url_for('homepage'))
    return render_template('register.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = float(request.form['deposit'])
        user.deposit(amount)
    balance = user.view_money()
    return render_template('deposit.html', balance=balance)

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'user' not in session:
        return redirect(url_for('login'))
    message = ""
    if request.method == 'POST':
        amount = float(request.form['withdraw'])
        message = user.withdraw(amount)
    balance = user.view_money()
    return render_template('withdraw.html', balance=balance, message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('homepage'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__('os').environ.get('PORT', 5000)), debug=True)
