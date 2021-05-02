from app import db
from .model import Model

class CodeVerification(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    code = db.Column(db.String(5),nullable=False)
    email = db.Column(db.String(100),nullable=False)

