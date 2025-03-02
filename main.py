from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from queue import Queue
import threading
import time
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testuser:BboZTLEtAdoIyzgIqZ8oVYZl1mdHYYgO@dpg-cv1vdp56l47c73fjgtmg-a.singapore-postgres.render.com/ecommerce_2jga'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
order_queue = Queue()

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    item_ids = db.Column(db.JSON, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def process_orders():
    """Background order processing worker"""
    while True:
        order_id = order_queue.get()
        with app.app_context():
            order = Order.query.get(order_id)
            order.status = 'Processing'
            order.updated_at = datetime.datetime.utcnow()
            db.session.commit()

            # Simulate processing time
            time.sleep(5)  

            order.status = 'Completed'
            order.updated_at = datetime.datetime.utcnow()
            db.session.commit()
        order_queue.task_done()

# Start worker thread
threading.Thread(target=process_orders, daemon=True).start()

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        order_id=data['order_id'],
        user_id=data['user_id'],
        item_ids=data['item_ids'],
        total_amount=data['total_amount']
    )
    db.session.add(new_order)
    db.session.commit()
    order_queue.put(data['order_id'])
    return jsonify({'order_id': data['order_id'], 'status': 'Pending'}), 202

@app.route('/orders/<order_id>/status', methods=['GET'])
def get_status(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({'status': order.status})

@app.route('/metrics', methods=['GET'])
def get_metrics():
    # Total orders
    total = Order.query.count()
    
    # Status counts
    status_counts = db.session.query(
        Order.status,
        db.func.count(Order.status)
    ).group_by(Order.status).all()
    
    # Average processing time
    avg_time = db.session.query(
        db.func.avg(Order.updated_at - Order.created_at)
    ).filter(Order.status == 'Completed').scalar()
    
    return jsonify({
        'total_orders': total,
        'status_counts': dict(status_counts),
        'average_processing_time': avg_time.total_seconds() if avg_time else 0
    })

if __name__ == '__main__':
    db.create_all()
    app.run(threaded=True)