from flask_login import UserMixin
from . import db
 
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000)) 

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))
    trip = db.Column(db.String(1000)) 
    startdate = db.Column(db.String(100))
    enddate = db.Column(db.String(100))
 
class Items(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1000))
    item = db.Column(db.String(100))
    price = db.Column(db.Integer)
    date = db.Column(db.String(100))
    tripId = db.Column(db.String(1000))

