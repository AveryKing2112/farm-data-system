select * from "Main".weather_weekly
with (timescaledb.continuous) as
select 
	time_bucket ('7 days', recorded_at) as week,
	AVG(temp_f) AS avg_temp_f,
    AVG(humidity_percent) AS avg_humidity,
    AVG(wind_mph) AS avg_wind_mph,
    SUM(precip_inches) AS total_precip,
    AVG(pressure_hpa) AS avg_pressure_hpa
FROM "Main".weather_data
GROUP BY time_bucket('7 days', recorded_at);



SELECT * FROM "Main".weather_weekly ORDER BY week DESC;
