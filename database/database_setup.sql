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


