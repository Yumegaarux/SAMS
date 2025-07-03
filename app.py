from flask import Flask, render_template, url_for
from models.db import db
import matplotlib.pyplot as plt
import io
import base64

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
    dates = [log.datetime for log in logs]
    values = [log.data for log in logs]

    plt.figure(figsize=(10, 4))
    plt.plot(dates, values, marker='o')
    plt.title('Sensor Data Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sensor Reading')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()

    return render_template('history.html', logs=logs, plot_url=plot_data)

@app.route("/help")
def help():
    return render_template('help.html')


if __name__ == "__main__":
    app.run(debug=True)