from flask import Blueprint, jsonify, request
from app import db
from app.models import Order
from app.services import order_queue
from app.model_helper import order_exists
from app.services import create_new_order

order_bp = Blueprint("order", __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    if 'order_id' not in data or 'user_id' not in data or 'item_ids' not in data or 'total_amount' not in data:
        return jsonify({'status': 'failed', 'error': 'missing parameter'}), 400
    id_exists = order_exists(data["order_id"])
    print("id_status : ", id_exists)
    if id_exists:
        return jsonify({'status': 'failed', 'error': 'order_id exists'}), 400
    order_data = create_new_order(data)
    if order_data:
        return jsonify({'order_id': data['order_id'], 'status': 'Pending'}), 202
    else:
        return jsonify({'status': 'failed', 'error': 'order creation failed'}), 500

@order_bp.route('/orders/<order_id>/status', methods=['GET'])
def get_status(order_id):
    # id_exists = order_exists(data["order_id"])
    order = Order.query.get_or_404(order_id)
    return jsonify({'status': order.status})

@order_bp.route('/metrics', methods=['GET'])
def get_metrics():
    total = Order.query.count()
    status_counts = db.session.query(Order.status, db.func.count(Order.status)).group_by(Order.status).all()
    avg_time = db.session.query(db.func.avg(Order.updated_at - Order.created_at)).filter(Order.status == 'Completed').scalar()
    
    return jsonify({
        'total_orders': total,
        'status_counts': dict(status_counts),
        'average_processing_time': avg_time.total_seconds() if avg_time else 0
    })

@order_bp.route('/metrics/<order_id>', methods=['GET'])
def get_order_metric(order_id):
    order = Order.query.get_or_404(order_id)
    response = {
        'order_id': order.order_id,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'updated_at': order.updated_at.isoformat()
    }
    if order.status == 'Completed':
        response['processing_time'] = f"{(order.updated_at - order.created_at).total_seconds():.2f} seconds"
    
    return jsonify(response)
