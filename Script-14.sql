CREATE TABLE "Main".weather_summaries (
    id SERIAL PRIMARY KEY,
    week_start DATE,
    week_end DATE,
    avg_temp_f NUMERIC,
    avg_humidity NUMERIC,
    avg_wind_mph NUMERIC,
    total_precip_inches NUMERIC,
    avg_pressure_hpa NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);