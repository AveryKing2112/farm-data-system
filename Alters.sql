alter table "Main".grow_cycles 
alter column start_date drop not null;

alter table "Main".crops
add column source_type varchar(50);