    
create table plots (
	id serial primary key,
	name varchar(100) not null,
	description text,
	area_sqft numeric,
	location_notes text,
	soil_notes text,
	is_active boolean default true,
	created_at timestamp default now()
	);

create table crops (
	id serial primary key,
	common_name varchar(100),
	variety varchar (100),
	seed_source varchar(100),
	days_to_maturity int,
	is_perennial boolean default false,
	notes text
	);

create table grow_cycles (	
	id serial primary key,
	plot_id int references plots(id),
	crop_id int references crops(id),
	status varchar(50) default 'active',
	start_date date,
	transplant_date date,
	actual_harvest_date date,
	notes text
	);

create table inputs_applied
id serial primary key,
grow_cycle_id int references grow_cycles(id),
date_applied date,
input_name varchar(100),
quantity_applied numeric,
quantity_unit varchar(50),
dilution_rate varchar(50),
application_method varchar(100),
notes text
);

create table oberservations (
	id serial primary key
	grow_cycle_id int references grow_cycles(id),
	observed_at timestamp default now(),
	oberservation_type varchar(100),
	value_numeric numeric,
	value_text text,
	noes text
	);

create table weather_data(
id serial primary key,
recorded_at timestamp,
temp_f numeric,
humidity_percent numeric,
precip_inches numeric,
wind_mph numeric,
conditions varchar(100),
source varchar(50) default 'openweathermap'
);