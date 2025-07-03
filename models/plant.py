from models.db import db 

class Plant(db.Model):
    __tablename__ = 'plant'

    plantID = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(30))
    minSalinityTol = db.Column(db.Float)
    maxSalinityTol = db.Column(db.Float)
    minpHTol = db.Column(db.Float)
    maxpHTol = db.Column(db.Float)
    wateringFrequencyReq = db.Column(db.Integer)
    recHarvestPeriod = db.Column(db.Integer)
