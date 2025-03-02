
Introduction:
This Project contains a sample ecommerce backend to create order and process the order in the background untill completion and generate order and process metrics.


Key Design:
API Framework:  Used Flask
Database: PostgreSQL, scales better for high concurrency
Queue: queue.Queue. A background worker (daemon) runs always checking to queue and processing the pending orders.
Worker Model: Background task running a loop. Simple and sufficient for 1,000 orders but may need multiprocessing for higher scalability.

Files:
main.py: contains app framework
config.py: contains db and other configs required
init.py: contains intialisation of framework and background workers
models.py: contains the schema definition
routes: contains API definitions
services.py: contains all service level implementation including queues
schema.sql: contain SQL scripts for schema creation and sample data population.


Key Design Decisions:
Concurrency Handling:

Flask threaded=True mode to handle concurrent requests
Separate worker thread for order processing 
PostgreSQL for concurrent database access
implemented connection polling to limit parallel active DB connections

Queue Implementation:
Python queue.Queue for in-memory queuing
Background worker processes orders sequentially
Automatic recovery of pending orders on restart

Trade-offs & Assumptions

Queue Persistence:
In-memory queue means orders are lost on server restart
Mitigated by re-enqueuing pending orders at startup

Scalability Limits:
Single-node deployment limits horizontal scaling
Multiple Gunicorn workers have separate queues

Processing Guarantees:
At-least-once delivery (orders might be processed multiple times after failures)


SAMPLE API curl and reponses:

1. Create Order API:
curl --location 'http://127.0.0.1:5000/orders' \
--header 'Content-Type: application/json' \
--data '{
    "order_id" : "11",
    "user_id" : "user_id",
    "item_ids" : "item_ids",
    "total_amount" :  100
}'
response: {
    "order_id": "11",
    "status": "Pending"
}

2. Order Status API:
curl --location 'http://127.0.0.1:5000/orders/3/status'
response:
{
    "status": "Completed"
}

3. Metrics API:
curl --location 'https://ecommerce-test-1-hlvi.onrender.com/metrics'
reponse:
{
    "average_processing_time": 2282.68599,
    "status_counts": {
        "Completed": 13,
        "Pending": 1
    },
    "total_orders": 14
}

4. Metrics Order API:
curl --location 'https://ecommerce-test-1-hlvi.onrender.com/metrics/11'

reponse: 
{
    "created_at": "2025-03-02T14:15:44.685458",
    "order_id": "11",
    "processing_time": "6.24 seconds",
    "status": "Completed",
    "updated_at": "2025-03-02T14:15:50.921274"
}

NB: The service is hosted on a free tier of onrender.com platform. Hence during inactivity the service goes down, So the first call longer time to get the response. Subsequent calls take lesser time.
USE below IPs in case of any issue:
13.228.225.19
18.142.128.26
54.254.162.138
followed by port 10000