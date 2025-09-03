CREATE TABLE IF NOT EXISTS insurance_users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    date_of_birth DATE,
    policy_number VARCHAR(20) UNIQUE NOT NULL,
    policy_type VARCHAR(20) CHECK (policy_type IN ('Auto', 'Home', 'Life', 'Health', 'Business')) NOT NULL,
    premium_amount DECIMAL(10, 2),
    policy_start_date DATE,
    policy_end_date DATE,
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(30),
    zip_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);