select avg(precip_inches) as average_rainfall
from "Main".weather_data
where recorded_at between '2026-04-01' and '2026-07-10';





select recorded_at, AVG(precip_inches) as average_rainfall_by_day
from "Main".weather_data
where recorded_at between '2026-04-01' and '2026-07-10';



select SUM(precip_inches) as total_rainfall
from "Main".weather_data
where recorded_at between '2026-05-01' and '2026-05-30'
and extract(minute from recorded_at) = 0;


SELECT SUM(precip_inches * 0.5) AS total_rainfall
FROM "Main".weather_data
WHERE recorded_at BETWEEN '2026-05-01' AND '2026-05-30';






WITH HourlyReadings AS (
    -- This section grabs exactly one reading per hour block to prevent double-counting
    SELECT DISTINCT ON (date_trunc('hour', recorded_at))
           date_trunc('hour', recorded_at) AS hour_block,
           precip_inches -- (Remember, this is actually mm!)
    FROM "Main".weather_data
    WHERE recorded_at BETWEEN '2026-06-01' AND '2026-06-30'
    ORDER BY date_trunc('hour', recorded_at), recorded_at DESC
)
-- This section sums those hourly readings and converts mm to inches
SELECT (SUM(precip_inches) / 25.4) AS total_rainfall_inches
FROM HourlyReadings;

