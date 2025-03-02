import time
import datetime
from queue import Queue
from app import db
from app.models import Order


order_queue = Queue()

def get_and_queue_pending_orders(app):
    """Retrieve all order IDs with status 'Pending' and add them to the queue."""
    with app.app_context():  # Ensure the database has an application context
        pending_orders = [order_id for (order_id,) in db.session.query(Order.order_id).filter_by(status='Pending').all()]
        for order_id in pending_orders:
            order_queue.put(order_id)
        print("queue : " , list(order_queue.queue))


def process_orders(app):
    """Background worker to process orders."""
    with app.app_context():  # Explicitly set app context
        print("order_queue : ", order_queue)
        while True:
            print("Processing order loop..")
            order_id = order_queue.get()
            print("order_id : ", order_id)

            with db.session.begin():
                order = Order.query.get(order_id)
                print(f"Processing order: {order_id}...")
                if order:
                    order.status = 'Processing'
                    order.updated_at = datetime.datetime.utcnow()
            
            time.sleep(5)  # Simulate processing time
            
            with db.session.begin():
                order = Order.query.get(order_id)
                if order:
                    order.status = 'Completed'
                    order.updated_at = datetime.datetime.utcnow()
                print(f"order_id : {order_id} processing complete")

            order_queue.task_done()


def process_orders_v2(app):
    # get_and_queue_pending_orders(order_queue)
    print("order_queue : ", )
    while True:
        print("processing order loop..")
        order_id = order_queue.get()
        print("order_id : ", order_id)
        with db.session.begin():
            order = Order.query.get(order_id)
            print("processing order : order_id : ", order_id, "processing...")
            if order:
                order.status = 'Processing'
                order.updated_at = datetime.datetime.utcnow()
        
        time.sleep(5)  # Simulate processing time
        
        with db.session.begin():
            order = Order.query.get(order_id)
            if order:
                order.status = 'Completed'
                order.updated_at = datetime.datetime.utcnow()
            print("order_id : ", order_id, "processing complete")
        
        order_queue.task_done()


def create_new_order(data):
    try:
        new_order = Order(
            order_id=data['order_id'],
            user_id=data['user_id'],
            item_ids=data['item_ids'],
            total_amount=data['total_amount']
        )
        db.session.add(new_order)
        db.session.commit()

        # add the order to the processing queue
        order_queue.put(data['order_id'])
        return True
    except Exception as e:
        return False
