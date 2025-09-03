CREATE TABLE IF NOT EXISTS policies_summ (
    policy_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    policy_number VARCHAR(20) UNIQUE NOT NULL,
    policy_type VARCHAR(20) CHECK (policy_type IN ('Auto', 'Home', 'Life', 'Health', 'Business')) NOT NULL,
    policy_status VARCHAR(20) CHECK (policy_status IN ('Active', 'Expired', 'Cancelled', 'Pending')) DEFAULT 'Active',
    premium_amount DECIMAL(10, 2) NOT NULL,
    coverage_amount DECIMAL(12, 2),
    deductible_amount DECIMAL(8, 2),
    policy_start_date DATE NOT NULL,
    policy_end_date DATE NOT NULL,
    payment_frequency VARCHAR(20) CHECK (payment_frequency IN ('Monthly', 'Quarterly', 'Semi-Annual', 'Annual')) DEFAULT 'Annual',
    agent_name VARCHAR(100),
    agent_phone VARCHAR(15),
    policy_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);