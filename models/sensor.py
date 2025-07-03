from app import db

class Sensor(db.Model):
    __tablename__ = 'sensor'

    sensorID = db.Column(db.Integer, primary_key=True)
    sensorName = db.Column(db.String(30))
