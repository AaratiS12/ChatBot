"""
PostgresDB
"""
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
from app import db

class chatmessages(db.Model):
    """Create table chatmessages"""
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300))

    def __init__(self, a):
        self.message = a

    def __repr__(self):
        return "<Message: %s>" % self.message
