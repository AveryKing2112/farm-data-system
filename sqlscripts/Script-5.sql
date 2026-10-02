set search_path to Main;
CREATE TABLE plots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    area_sqft NUMERIC,
    location_notes TEXT,
    soil_notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE crops (
    id SERIAL PRIMARY KEY,
    common_name VARCHAR(100),
    variety VARCHAR(100),
    seed_source VARCHAR(100),
    days_to_maturity INT,
    is_perennial BOOLEAN DEFAULT FALSE,
    notes TEXT
);

CREATE TABLE grow_cycles (
    id SERIAL PRIMARY KEY,
    plot_id INT REFERENCES plots(id),
    crop_id INT REFERENCES crops(id),
    status VARCHAR(50) DEFAULT 'active',
    start_date DATE,
    transplant_date DATE,
    expected_harvest_date DATE,
    actual_harvest_date DATE,
    notes TEXT
);

CREATE TABLE inputs_applied (
    id SERIAL PRIMARY KEY,
    grow_cycle_id INT REFERENCES grow_cycles(id),
    date_applied DATE,
    input_name VARCHAR(100),
    quantity_applied NUMERIC,
    quantity_unit VARCHAR(50),
    dilution_rate VARCHAR(50),
    application_method VARCHAR(100),
    notes TEXT
);

CREATE TABLE observations (
    id SERIAL PRIMARY KEY,
    grow_cycle_id INT REFERENCES grow_cycles(id),
    observed_at TIMESTAMP DEFAULT NOW(),
    observation_type VARCHAR(100),
    value_numeric NUMERIC,
    value_text TEXT,
    notes TEXT
);

CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    recorded_at TIMESTAMP,
    temp_f NUMERIC,
    humidity_percent NUMERIC,
    precip_inches NUMERIC,
    wind_mph NUMERIC,
    conditions VARCHAR(100),
    source VARCHAR(50) DEFAULT 'openweathermap'
);