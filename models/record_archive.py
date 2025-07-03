from models.db import db 

class RecordArchive(db.Model):
    __tablename__ = 'record_archive'

    RAID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    avgpHlevel = db.Column(db.Float)
    avgSalinity = db.Column(db.Float)
    remarks = db.Column(db.String(100))
