from models.db import db 

class User(db.Model):
    __tablename__ = 'user'

    userID = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(30))
    fname = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(60))
    contact_number = db.Column(db.String(11))