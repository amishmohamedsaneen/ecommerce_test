from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


import threading

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    from app.routes import order_bp
    app.register_blueprint(order_bp)

    #daemon to process the order in the background
    from app.services import process_orders, get_and_queue_pending_orders
    get_and_queue_pending_orders(app)
    threading.Thread(target=process_orders, daemon=True, args =(app,)).start()

    return app
