from models.db import db 

class FishBatch(db.Model):
    __tablename__ = 'fish_batch'

    FBID = db.Column(db.Integer, primary_key=True)
    fishID = db.Column(db.Integer)
    minSalinity = db.Column(db.Float)
    maxSalinity = db.Column(db.Float)
    minpH = db.Column(db.Float)
    maxpH = db.Column(db.Float)
