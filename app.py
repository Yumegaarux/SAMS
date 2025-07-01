from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Controller for flask is app.py
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/control")
def control():
    return render_template('control.html')

@app.route("/history")
def history():
    return render_template('history.html')

@app.route("/help")
def help():
    return render_template('help.html')

if __name__ == "__main__":
    app.run(debug=True)