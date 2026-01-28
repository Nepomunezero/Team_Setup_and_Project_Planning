-- sample statments(queries) to insert data into our main tables

-- insert into customer table
INSERT INTO customers (full_name, phone_number, last_activity)
VALUES
('Alice Mukamana', '+250788111111', NOW()),
('Jean Uwimana', '+250788222222', NOW()),
('Eric Ndayishimiye', '+250788333333', NOW()),
('Claire Ingabire', '+250788444444', NOW()),
('David Habimana', '+250788555555', NOW());



-- sample data for tr_categories
INSERT INTO transaction_categories (category_name, category_code, category_fee)
VALUES
('Send Money', 'SEND_MONEY', 1),
('Buy Airtime', 'BUY_AIRTIME', 0),
('Buy Electricity', 'BUY_ELECTRICITY', 0),
('Pay Water Bill', 'PAY_WATER', 0),
('Pay School Fees', 'PAY_SCHOOL', 1);


-- sample data for transaction table

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

-- sample data for system_logs

INSERT INTO system_logs (
    log_type,
    log_source,
    user_id,
    log_time
)
VALUES
('INFO', 'SMS_PARSER', 1, NOW()),
('WARNING', 'TRANSACTION_ENGINE', 2, NOW()),
('ERROR', 'DATABASE_LAYER', 3, NOW()),
('DEBUG', 'FEE_CALCULATOR', 1, NOW()),
('INFO', 'USER_AUTH', 5, NOW());


