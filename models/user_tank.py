from app import db

class UserTank(db.Model):
    __tablename__ = 'user_tank'

    UTID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    tankID = db.Column(db.Integer)
