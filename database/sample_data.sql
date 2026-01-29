-- =====================================================
-- SAMPLE QUERIES FOR MOMO SMS DATABASE
-- Purpose: Test CRUD operations and analytics
-- =====================================================

-- -----------------------------------------------------
-- INSERT SAMPLE DATA
-- -----------------------------------------------------

-- Insert sample customers
INSERT INTO customers (full_name, phone_number, last_activity)
VALUES
('Alice Mukamana', '+250788111111', NOW()),
('Jean Uwimana', '+250788222222', NOW()),
('Eric Ndayishimiye', '+250788333333', NOW()),
('Claire Ingabire', '+250788444444', NOW()),
('David Habimana', '+250788555555', NOW());

-- Insert sample transaction categories
INSERT INTO transaction_categories (category_name, category_code, category_fee)
VALUES
('Send Money', 'SEND_MONEY', 1),
('Buy Airtime', 'BUY_AIRTIME', 0),
('Buy Electricity', 'BUY_ELECTRICITY', 0),
('Pay Water Bill', 'PAY_WATER', 0),
('Pay School Fees', 'PAY_SCHOOL', 1);

-- Insert sample transactions
INSERT INTO transactions (
    sender_id,
    receiver_id,
    category_id,
    amount,
    fee_amount,
    balance_after,
    created_at
)
VALUES
(1, 2, 1, 5000.00, 100.00, 14900.00, NOW()),
(2, 3, 1, 10000.00, 150.00, 39850.00, NOW()),
(1, 1, 2, 2000.00, 0.00, 12900.00, NOW()),
(3, 4, 3, 15000.00, 0.00, 50000.00, NOW()),
(5, 2, 5, 25000.00, 300.00, 75000.00, NOW());

-- Insert sample system logs
INSERT INTO system_logs (log_type, log_source, user_id, log_time)
VALUES
('INFO', 'SMS_PARSER', 1, NOW()),
('WARNING', 'TRANSACTION_ENGINE', 2, NOW()),
('ERROR', 'DATABASE_LAYER', 3, NOW()),
('DEBUG', 'FEE_CALCULATOR', 1, NOW()),
('INFO', 'USER_AUTH', 5, NOW());

-- -----------------------------------------------------
-- READ (SELECT) QUERIES
-- -----------------------------------------------------

-- View all transactions with related customer and category data
SELECT
    t.id AS transaction_id,
    sender.full_name AS sender_name,
    receiver.full_name AS receiver_name,
    c.category_name,
    t.amount,
    t.fee_amount,
    t.created_at
FROM transactions t
JOIN customers sender ON t.sender_id = sender.id
JOIN customers receiver ON t.receiver_id = receiver.id
JOIN transaction_categories c ON t.category_id = c.id
ORDER BY t.created_at DESC;

-- Get all transactions involving a specific customer
SELECT
    t.id,
    c.category_name,
    t.amount,
    t.created_at
FROM transactions t
JOIN transaction_categories c ON t.category_id = c.id
WHERE t.sender_id = 1 OR t.receiver_id = 1;

-- Count transactions per category
SELECT
    c.category_name,
    COUNT(t.id) AS total_transactions
FROM transaction_categories c
LEFT JOIN transactions t ON c.id = t.category_id
GROUP BY c.category_name;

-- -----------------------------------------------------
-- UPDATE QUERIES
-- -----------------------------------------------------

-- Update customer's last activity
UPDATE customers
SET last_activity = NOW()
WHERE id = 3;

-- Correct transaction fee
UPDATE transactions
SET fee_amount = 200.00
WHERE id = 2;

-- -----------------------------------------------------
-- DELETE QUERIES
-- -----------------------------------------------------

-- Delete old debug logs
DELETE FROM system_logs
WHERE log_type = 'DEBUG'
AND log_time < NOW() - INTERVAL 7 DAY;

-- Remove invalid transactions (example cleanup)
DELETE FROM transactions
WHERE amount = 0;

-- -----------------------------------------------------
-- ANALYTICAL / REPORTING QUERIES
-- -----------------------------------------------------

-- Total amount sent per customer
SELECT
    c.full_name,
    SUM(t.amount) AS total_sent
FROM customers c
JOIN transactions t ON c.id = t.sender_id
GROUP BY c.full_name
ORDER BY total_sent DESC;

-- Daily transaction summary
SELECT
    DATE(created_at) AS transaction_date,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY DATE(created_at)
ORDER BY transaction_date DESC;

-- Total fees collected per transaction category
SELECT
    c.category_name,
    SUM(t.fee_amount) AS total_fees_collected
FROM transaction_categories c
JOIN transactions t ON c.id = t.category_id
GROUP BY c.category_name;
