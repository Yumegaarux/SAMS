from app import db

class BatchBridge(db.Model):
    __tablename__ = 'batch_bridge'

    BBID = db.Column(db.Integer, primary_key=True)
    fishID = db.Column(db.Integer, nullable=False)
    FBID = db.Column(db.Integer, nullable=False)
