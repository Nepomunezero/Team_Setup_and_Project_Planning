CREATE DATABASE momo_sistem;
USE momo_system;


CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity DATETIME NOT NULL
);

CREATE TABLE transaction_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    category_code VARCHAR(20) NOT NULL,
    category_fee BOOLEAN NOT NULL
);


CREATE TABLE transactions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    fee_amount DECIMAL(10,2) NOT NULL,
    balance_after DECIMAL(12,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sender
        FOREIGN KEY (sender_id) REFERENCES customers(id),

    CONSTRAINT fk_receiver
        FOREIGN KEY (receiver_id) REFERENCES customers(id),

    CONSTRAINT fk_category
        FOREIGN KEY (category_id) REFERENCES transaction_categories(id)
);

CREATE TABLE system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    log_type ENUM('INFO', 'WARNING', 'ERROR', 'DEBUG') NOT NULL,
    log_source VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,

    CONSTRAINT fk_log_user
        FOREIGN KEY (user_id) REFERENCES customers(id)
);


CREATE TABLE sms_raw_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    data TEXT NOT NULL,
    created_at DATETIME NOT NULL,

    CONSTRAINT fk_sms_user
        FOREIGN KEY (user_id) REFERENCES customers(id)

);


CREATE TABLE user_relationships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id1 INT NOT NULL,
    user_id2 INT NOT NULL,
    relationship_type ENUM('SENDER', 'RECEIVER') NOT NULL,

    CONSTRAINT fk_user1
        FOREIGN KEY (user_id1) REFERENCES customers(id),

    CONSTRAINT fk_user2
        FOREIGN KEY (user_id2) REFERENCES customers(id),

    CONSTRAINT unique_relationship
        UNIQUE (user_id1, user_id2, relationship_type)
);



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

