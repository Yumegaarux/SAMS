from models.db import db 

class Fish(db.Model):
    __tablename__ = 'fish'

    fishID = db.Column(db.Integer, primary_key=True)
    fish_name = db.Column(db.String(30))
    minSalinityTol = db.Column(db.Float)
    maxSalinityTol = db.Column(db.Float)
    minpHTol = db.Column(db.Float)
    maxpHTol = db.Column(db.Float)
    feedingFrequencyReq = db.Column(db.Integer)
    recHarvestPeriod = db.Column(db.Integer)
