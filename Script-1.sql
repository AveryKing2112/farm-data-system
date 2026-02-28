create table inputs_log (
	input_id 	serial primary key,
	input_type 	text not null, 
	batch_date 	date default current_date,
	dilution 	text,
	is_powder 	boolean default false,
	notes 		text
);