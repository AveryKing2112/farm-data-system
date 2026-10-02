--- Agritech Farm Database
--- Author: Avery King
--- Created: 2/27/2026
--- Combined schema: includes all changes previously in Alters.sql
--- Run this on a fresh database to create every table.

-- TimescaleDB is needed for the weather_data hypertable
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE SCHEMA IF NOT EXISTS "Main";


-------------------------------------------------------------
-- Plots, crops, and grow cycles
-------------------------------------------------------------

CREATE TABLE "Main".plots (
    plot_id         SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    area_sqft       NUMERIC,
    location_notes  TEXT,
    soil_notes      TEXT,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE "Main".crops (
    crop_id           SERIAL PRIMARY KEY,
    common_name       VARCHAR(100),
    variety           VARCHAR(100),
    seed_source       VARCHAR(100),
    days_to_maturity  INT,
    is_perennial      BOOLEAN DEFAULT FALSE,
    notes             TEXT,
    source_type       VARCHAR(50),
    species           VARCHAR(100)
);

CREATE TABLE "Main".grow_cycles (
    grow_cycle_id          SERIAL PRIMARY KEY,
    plot_id                INT REFERENCES "Main".plots(plot_id),
    crop_id                INT REFERENCES "Main".crops(crop_id),
    status                 VARCHAR(50) DEFAULT 'active',
    start_date             DATE,
    transplant_date        DATE,
    expected_harvest_date  DATE,
    actual_harvest_date    DATE,
    notes                  TEXT,
    sow_method             VARCHAR(20),
    direct_sow_date        DATE,
    is_control             BOOLEAN DEFAULT FALSE
);

-- Individual plants within a grow cycle, for controlled comparisons
CREATE TABLE "Main".cycle_plants (
    plant_id       SERIAL PRIMARY KEY,
    grow_cycle_id  INT REFERENCES "Main".grow_cycles(grow_cycle_id),
    row_num        INT,
    pos_num        INT,
    status         TEXT DEFAULT 'Alive' CHECK (status IN ('Alive', 'Dead', 'Harvested')),
    plot_id        INT REFERENCES "Main".plots(plot_id)
);


-------------------------------------------------------------
-- Inputs and observations
-------------------------------------------------------------

CREATE TABLE "Main".inputs_applied (
    input_id            SERIAL PRIMARY KEY,
    grow_cycle_id       INT REFERENCES "Main".grow_cycles(grow_cycle_id),
    date_applied        DATE,
    input_name          VARCHAR(100),
    quantity_applied    NUMERIC,
    quantity_unit       VARCHAR(50),
    dilution_rate       VARCHAR(50),
    application_method  VARCHAR(100),
    notes               TEXT,
    input_amount_ml     NUMERIC,
    water_amount_ml     NUMERIC
);

-- Batches of inputs made (JLF, LAB, FPJ, etc.)
CREATE TABLE "Main".inputs_log (
    input_id    SERIAL PRIMARY KEY,
    input_type  TEXT NOT NULL,
    batch_date  DATE DEFAULT CURRENT_DATE,
    dilution    TEXT,
    is_powder   BOOLEAN DEFAULT FALSE,
    notes       TEXT
);

CREATE TABLE "Main".observations (
    observation_id    SERIAL PRIMARY KEY,
    grow_cycle_id     INT REFERENCES "Main".grow_cycles(grow_cycle_id),
    observed_at       TIMESTAMP DEFAULT NOW(),
    observation_type  VARCHAR(100),
    value_numeric     NUMERIC,
    value_text        TEXT,
    notes             TEXT,
    plant_label       VARCHAR(50)
);


-------------------------------------------------------------
-- Ferments
-------------------------------------------------------------

CREATE TABLE "Main".ferments (
    ferment_id    SERIAL PRIMARY KEY,
    name          VARCHAR(100),
    ferment_type  VARCHAR(100),
    stage         VARCHAR(100),
    started_at    DATE,
    completed_at  DATE,
    status        VARCHAR(50) DEFAULT 'active',
    vessel_size   VARCHAR(50),
    notes         TEXT
);

CREATE TABLE "Main".ferment_logs (
    ferment_log_id  SERIAL PRIMARY KEY,
    ferment_id      INT REFERENCES "Main".ferments(ferment_id),
    logged_at       TIMESTAMP DEFAULT NOW(),
    stage           VARCHAR(100),
    temp_f          NUMERIC,
    action_taken    TEXT,
    observations    TEXT,
    notes           TEXT
);


-------------------------------------------------------------
-- Weather and climate
-------------------------------------------------------------

-- Hypertables need the time column in the primary key
CREATE TABLE "Main".weather_data (
    id                SERIAL,
    recorded_at       TIMESTAMP NOT NULL,
    temp_f            NUMERIC,
    temp_min_f        NUMERIC,
    temp_max_f        NUMERIC,
    feels_like_f      NUMERIC,
    humidity_percent  NUMERIC,
    pressure_hpa      NUMERIC,
    sea_level_hpa     NUMERIC,
    ground_level_hpa  NUMERIC,
    visibility_m      NUMERIC,
    precip_inches     NUMERIC,
    wind_mph          NUMERIC,
    conditions        VARCHAR(100),
    sunrise           TIMESTAMP,
    sunset            TIMESTAMP,
    source            VARCHAR(50) DEFAULT 'openweathermap',
    PRIMARY KEY (id, recorded_at)
);

SELECT create_hypertable('"Main".weather_data', 'recorded_at');

CREATE TABLE "Main".weather_summaries (
    id                   SERIAL PRIMARY KEY,
    week_start           DATE,
    week_end             DATE,
    avg_temp_f           NUMERIC,
    avg_humidity         NUMERIC,
    avg_wind_mph         NUMERIC,
    total_precip_inches  NUMERIC,
    avg_pressure_hpa     NUMERIC,
    created_at           TIMESTAMP DEFAULT NOW()
);

-- Frost events, heat waves, storms, etc.
CREATE TABLE "Main".climate_events (
    event_id    SERIAL PRIMARY KEY,
    event_name  TEXT,
    start_time  TIMESTAMPTZ,
    end_time    TIMESTAMPTZ,
    min_temp    DOUBLE PRECISION,
    notes       TEXT
);
