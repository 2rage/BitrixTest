from .database import db

class Superhero(db.Model):
    __tablename__ = 'superheroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    intelligence = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    power = db.Column(db.Integer)
    appearances = db.relationship('Appearance', backref='superhero', lazy=True)

class Appearance(db.Model):
    __tablename__ = 'appearances'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(50))
    race = db.Column(db.String(50))
    height = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    hero_id = db.Column(db.Integer, db.ForeignKey('superheroes.id'), nullable=False)
