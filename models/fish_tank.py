from models.db import db 

class FishTank(db.Model):
    __tablename__ = 'fish_tank'

    tankID = db.Column(db.Integer, primary_key=True)
    FBID = db.Column(db.Integer)
    plantID = db.Column(db.Integer)
    minSalinity = db.Column(db.Float)
    maxSalinity = db.Column(db.Float)
    minpH = db.Column(db.Float)
    maxpH = db.Column(db.Float)
