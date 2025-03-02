from app import db
from app.models import Order

def order_exists(order_id):
    """Check if an order with the given order_id exists in the database."""
    return db.session.query(Order.query.filter_by(order_id=order_id).exists()).scalar()


