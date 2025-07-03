from app import db

class Notification(db.Model):
    __tablename__ = 'notification'

    notifID = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    alert = db.Column(db.String(30))
    suggestion = db.Column(db.String(50))
