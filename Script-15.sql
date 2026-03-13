select (temp_f) from "Main".weather_data
where recorded_at >= now() - interval '7 days';


select AVG(temp_f), AVG(humidity_percent), AVG(precip_inches), AVG(wind_mph), AVG(pressure_hpa) FROM "Main".weather_data
where recorded_at >= NOW() - INTERVAL '7 days';