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





ALTER TABLE "Main".plots RENAME COLUMN id TO plot_id;
ALTER TABLE "Main".crops RENAME COLUMN id TO crop_id;
ALTER TABLE "Main".grow_cycles RENAME COLUMN id TO grow_cycle_id;
ALTER TABLE "Main".observations RENAME COLUMN id TO observation_id;
ALTER TABLE "Main".inputs_applied RENAME COLUMN id TO input_id;
ALTER TABLE "Main".ferments RENAME COLUMN id TO ferment_id;
ALTER TABLE "Main".ferment_logs RENAME COLUMN id TO ferment_log_id;