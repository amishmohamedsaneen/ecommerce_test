


Key Design Decisions
Concurrency Handling:

Flask threaded=True mode to handle concurrent requests
Separate worker thread for order processing 
PostgreSQL for concurrent database access

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
Multiple Gunicorn workers have separate queues (use Redis in production)

Processing Guarantees:
At-least-once delivery (orders might be processed multiple times after failures)