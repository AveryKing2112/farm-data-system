select recorded_at, temp_f
from "Main".weather_data
where temp_f <= 34
	and recorded_at >= '2026-03-17'
order by recorded_at asc;


create table climate_events (
	event_id 	serial primary key,
	event_name 	text,
	start_time 	timestamptz,
	end_time 	timestamptz,
	min_temp 	double precision,
	notes 		text
	);




INSERT INTO climate_events (event_name, start_time, end_time, min_temp, notes)
VALUES (
    'March Surprise Freeze', 
    '2026-03-17 06:02:00-04', 
    '2026-03-19 07:02:00-04', 
    33.0, 
    'Seedlings emerged but survived with very limited makeshift covers. Zone 8b freaks.'
);