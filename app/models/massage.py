from ..extensions import db

class Massage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_of_massage = db.Column(db.String(100))
    massage = db.Column(db.String(10000))