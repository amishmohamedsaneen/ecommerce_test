-- schema.sql
-- Create orders table
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    item_ids JSONB NOT NULL,
    total_amount FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sample data insertion
INSERT INTO orders (order_id, user_id, item_ids, total_amount, status, created_at, updated_at)
VALUES 
    ('ORD1001', 'USR2023', '["ITEM001", "ITEM005"]', 149.99, 'Completed', 
     '2023-10-01 08:00:00+00', '2023-10-01 08:05:23+00'),
    
    ('ORD1002', 'USR2023', '["ITEM012"]', 79.99, 'Processing', 
     '2023-10-01 09:15:00+00', '2023-10-01 09:15:00+00'),
    
    ('ORD1003', 'USR4567', '["ITEM007", "ITEM008", "ITEM009"]', 299.95, 'Pending', 
     '2023-10-01 10:30:00+00', '2023-10-01 10:30:00+00'),
    
    ('ORD1004', 'USR7890', '["ITEM003"]', 49.99, 'Completed', 
     '2023-10-01 11:45:00+00', '2023-10-01 11:47:15+00'),
    
    ('ORD1005', 'USR1234', '["ITEM002", "ITEM004"]', 199.50, 'Completed', 
     '2023-10-01 12:00:00+00', '2023-10-01 12:03:45+00');

-- Update the updated_at for processing order to simulate in-progress
UPDATE orders SET updated_at = '2023-10-01 09:17:30+00' 
WHERE order_id = 'ORD1002';