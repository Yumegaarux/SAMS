from models.db import db 

class ActivityArchive(db.Model):
    __tablename__ = 'activity_archive'

    AAID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    activity = db.Column(db.String(30))
