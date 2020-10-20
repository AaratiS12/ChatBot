import flask_sqlalchemy
from app import db


class chatmessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300))
    
    def __init__(self, a):
        self.message = a
        
    def __repr__(self):
        return '<Message: %s>' % self.message 

