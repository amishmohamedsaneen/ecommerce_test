import datetime
from app import db

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    item_ids = db.Column(db.JSON, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
