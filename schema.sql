CREATE TABLE parking_lots (
    lot_id INT AUTO_INCREMENT PRIMARY KEY,
    lot_name VARCHAR(100) NOT NULL,
    total_capacity INT NOT NULL,
    available_slots INT NOT NULL,
    currency VARCHAR(10) DEFAULT 'KES'
);

CREATE TABLE parking_bays (
    bay_id INT AUTO_INCREMENT PRIMARY KEY,
    lot_id INT NOT NULL,
    bay_number VARCHAR(20) NOT NULL UNIQUE,
    is_occupied BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (lot_id) REFERENCES parking_lots(lot_id)
);

CREATE TABLE tariff_rates (
    rate_id INT AUTO_INCREMENT PRIMARY KEY,
    lot_id INT NOT NULL,
    base_rate DECIMAL(8,2) NOT NULL,
    hourly_rate DECIMAL(8,2) NOT NULL,
    grace_period_minutes INT DEFAULT 15,
    vat_percentage DECIMAL(5,2) DEFAULT 16.00,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (lot_id) REFERENCES parking_lots(lot_id)
);

CREATE TABLE parking_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    lot_id INT NOT NULL,
    bay_number VARCHAR(20) NOT NULL,
    plate_number VARCHAR(20) NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    is_override BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (lot_id) REFERENCES parking_lots(lot_id)
);

CREATE TABLE payment_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    net_amount DECIMAL(8,2) NOT NULL,
    vat_amount DECIMAL(8,2) NOT NULL,
    gross_amount DECIMAL(8,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    mpesa_receipt_number VARCHAR(50) NULL,
    payment_time DATETIME NOT NULL,
    FOREIGN KEY (session_id) REFERENCES parking_sessions(session_id)
);

CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    performed_at DATETIME NOT NULL
);