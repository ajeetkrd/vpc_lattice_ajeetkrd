INSERT INTO policies_summ (
    user_id, policy_number, policy_type, policy_status, premium_amount, 
    coverage_amount, deductible_amount, policy_start_date, policy_end_date, 
    payment_frequency, agent_name, agent_phone, policy_description
) VALUES 
(
    1, 'AUTO001234', 'Auto', 'Active', 1200.00, 50000.00, 500.00,
    '2024-01-15', '2025-01-14', 'Semi-Annual',
    'Mike Thompson', '555-2001', 'Full coverage auto insurance for 2022 Honda Civic'
),
(
    2, 'HOME005678', 'Home', 'Active', 850.00, 300000.00, 1000.00,
    '2024-02-01', '2025-01-31', 'Annual',
    'Lisa Rodriguez', '555-2002', 'Homeowners insurance for single family home'
),
(
    3, 'LIFE009012', 'Life', 'Active', 2400.00, 500000.00, 0.00,
    '2024-03-10', '2025-03-09', 'Quarterly',
    'Robert Chen', '555-2003', 'Term life insurance policy - 20 year term'
),
(
    4, 'HEALTH003456', 'Health', 'Active', 3600.00, 1000000.00, 2500.00,
    '2024-01-01', '2024-12-31', 'Monthly',
    'Sarah Williams', '555-2004', 'Comprehensive health insurance with dental and vision'
),
(
    5, 'BUS007890', 'Business', 'Active', 4800.00, 2000000.00, 5000.00,
    '2024-04-01', '2025-03-31', 'Quarterly',
    'David Park', '555-2005', 'General liability and property insurance for tech startup'
),
(
    6, 'AUTO001235', 'Auto', 'Active', 1350.00, 75000.00, 750.00,
    '2024-05-15', '2025-05-14', 'Semi-Annual',
    'Jennifer Lee', '555-2006', 'Premium auto coverage for 2023 BMW X5'
),
(
    7, 'HOME005679', 'Home', 'Active', 950.00, 450000.00, 1500.00,
    '2024-06-01', '2025-05-31', 'Annual',
    'Mark Johnson', '555-2007', 'Homeowners insurance with flood coverage'
),
(
    8, 'LIFE009013', 'Life', 'Pending', 1800.00, 250000.00, 0.00,
    '2024-02-20', '2025-02-19', 'Annual',
    'Emily Davis', '555-2008', 'Whole life insurance policy with investment component'
),
(
    9, 'HEALTH003457', 'Health', 'Active', 4200.00, 500000.00, 3000.00,
    '2024-03-01', '2025-02-28', 'Monthly',
    'Carlos Martinez', '555-2009', 'Premium health plan with specialist coverage'
),
(
    10, 'AUTO001236', 'Auto', 'Active', 1100.00, 40000.00, 250.00,
    '2024-07-10', '2025-07-09', 'Annual',
    'Amanda Wilson', '555-2010', 'Basic auto coverage for 2019 Toyota Corolla'
),
(
    1, 'HOME005680', 'Home', 'Expired', 780.00, 250000.00, 1000.00,
    '2023-01-15', '2024-01-14', 'Annual',
    'Mike Thompson', '555-2001', 'Previous homeowners policy - expired'
),
(
    3, 'AUTO001237', 'Auto', 'Cancelled', 1450.00, 60000.00, 1000.00,
    '2023-08-01', '2024-07-31', 'Monthly',
    'Robert Chen', '555-2003', 'Auto policy cancelled due to vehicle sale'
),
(
    5, 'HEALTH003458', 'Health', 'Active', 5200.00, 2000000.00, 1000.00,
    '2024-08-01', '2025-07-31', 'Monthly',
    'David Park', '555-2005', 'Executive health plan with concierge services'
),
(
    2, 'LIFE009014', 'Life', 'Active', 3200.00, 750000.00, 0.00,
    '2024-09-01', '2025-08-31', 'Semi-Annual',
    'Lisa Rodriguez', '555-2002', 'Universal life insurance with flexible premiums'
),
(
    4, 'AUTO001238', 'Auto', 'Pending', 1600.00, 80000.00, 500.00,
    '2024-12-01', '2025-11-30', 'Quarterly',
    'Sarah Williams', '555-2004', 'New auto policy for electric vehicle'
);