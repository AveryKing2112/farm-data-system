alter table "Main".weather_data 
add column temp_min_f numeric,
add column temp_max_f numeric,
add column feels_like_f numeric,
add column pressure_hpa numeric,
add column sea_level numeric,
add column ground_level_hpa numeric,
add column visibility_m numeric,
add column sunrise timestamp,
add column sunset timestamp;