from app import db
from .model import Model

class Image(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    ext = db.Column(db.String(100),nullable=False)

