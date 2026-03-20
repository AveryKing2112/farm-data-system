CREATE TABLE "Main".weather_data_backup AS SELECT * FROM "Main".weather_data;


drop table "Main".weather_data;


CREATE TABLE "Main".weather_data (
    id SERIAL,
    recorded_at TIMESTAMP NOT NULL,
    temp_f NUMERIC,
    temp_min_f NUMERIC,
    temp_max_f NUMERIC,
    feels_like_f NUMERIC,
    humidity_percent NUMERIC,
    pressure_hpa NUMERIC,
    sea_level_hpa NUMERIC,
    ground_level_hpa NUMERIC,
    visibility_m NUMERIC,
    precip_inches NUMERIC,
    wind_mph NUMERIC,
    conditions VARCHAR(100),
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    source VARCHAR(50) DEFAULT 'openweathermap'
);

SELECT create_hypertable('"Main".weather_data', 'recorded_at');

INSERT INTO "Main".weather_data 
SELECT 
    id,
    recorded_at,
    temp_f::NUMERIC,
    temp_min_f::NUMERIC,
    temp_max_f::NUMERIC,
    feels_like_f::NUMERIC,
    humidity_percent::NUMERIC,
    pressure_hpa::NUMERIC,
    sea_level_hpa::NUMERIC,
    ground_level_hpa::NUMERIC,
    visibility_m::NUMERIC,
    precip_inches::NUMERIC,
    wind_mph::NUMERIC,
    conditions,
    sunrise,
    sunset,
    source
FROM "Main".weather_data_backup;






CREATE MATERIALIZED VIEW "Main".weather_weekly
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('7 days', recorded_at) AS week,
    AVG(temp_f) AS avg_temp_f,
    AVG(humidity_percent) AS avg_humidity,
    AVG(wind_mph) AS avg_wind_mph,
    SUM(precip_inches) AS total_precip,
    AVG(pressure_hpa) AS avg_pressure_hpa
FROM "Main".weather_data
GROUP BY time_bucket('7 days', recorded_at);