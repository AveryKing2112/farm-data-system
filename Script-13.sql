CREATE TABLE "Main".ferments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    ferment_type VARCHAR(100),
    stage VARCHAR(100),
    started_at DATE,
    completed_at DATE,
    status VARCHAR(50) DEFAULT 'active',
    vessel_size VARCHAR(50),
    notes TEXT
);

CREATE TABLE "Main".ferment_logs (
    id SERIAL PRIMARY KEY,
    ferment_id INT REFERENCES "Main".ferments(id),
    logged_at TIMESTAMP DEFAULT NOW(),
    stage VARCHAR(100),
    temp_f NUMERIC,
    action_taken TEXT,
    observations TEXT,
    notes TEXT
);