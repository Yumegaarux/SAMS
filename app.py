from flask import Flask, render_template, url_for
from models.db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smartpond_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import *

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
    logs = SensorLog.query.order_by(SensorLog.datetime.desc()).all()
    return render_template('history.html', logs=logs)

@app.route("/help")
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.run(debug=True)