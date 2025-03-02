from app import create_app, db
from app.services import process_orders
from sqlalchemy.pool import QueuePool
import threading


app = create_app()
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,  # Limit the number of active connections
    'max_overflow': 5,  # Allow temporary connections beyond pool_size
    'pool_timeout': 30,  # Timeout for getting a connection from pool
    'pool_recycle': 1800  # Recycle connections after 30 minutes
}




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(threaded=True)
