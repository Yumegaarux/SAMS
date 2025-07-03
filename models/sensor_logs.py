from models.db import db 

class SensorLog(db.Model):
    __tablename__ = 'sensor_logs'

    SensorLogID = db.Column(db.Integer, primary_key=True)
    sensorID = db.Column(db.Integer)
    tankID = db.Column(db.Integer)
    data = db.Column(db.Float)
    datetime = db.Column(db.DateTime)
