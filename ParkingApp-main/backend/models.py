# app/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'

    id       = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    address  = db.Column(db.String(255), nullable=False)
    pincode  = db.Column(db.String(6),   nullable=False)
    role     = db.Column(db.String(10),  nullable=False, default='user')

    # A user can create many lots, and make many reservations
    created_lots  = db.relationship('ParkingLot',   backref='creator', lazy=True)
    reservations  = db.relationship('Reservation',   backref='user',    lazy=True)
class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(120), unique=True, nullable=False)
    location       = db.Column(db.String(255),              nullable=False)
    pincode        = db.Column(db.String(20),               nullable=False)
    price_per_hour = db.Column(db.Float,                    nullable=False)
    created_by     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spots         = db.relationship(
        'ParkingSpot',
        backref='lot',
        cascade='all, delete-orphan',
        lazy=True
    )
    reservations  = db.relationship('Reservation', backref='lot', lazy=True)
class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'

    id           = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id', ondelete='CASCADE'), nullable=False)
    spot_number  = db.Column(db.Integer,                     nullable=False)
    is_reserved  = db.Column(db.Boolean, default=False)

    reservations = db.relationship('Reservation', backref='spot', lazy=True)
class Reservation(db.Model):
    __tablename__ = 'reservation'
    
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lot_id         = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_id        = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    start_time     = db.Column(db.DateTime, default=datetime.utcnow)
    end_time       = db.Column(db.DateTime, nullable=True)
    released_at    = db.Column(db.DateTime, nullable=True)
    cost           = db.Column(db.Float, nullable=True)
    vehicle_number = db.Column(db.String(50), nullable=False)

    parking_spot = db.relationship(
    'ParkingSpot',
    backref='reservations_for_report',
    foreign_keys=[spot_id],
    overlaps="spot,reservations"
)


