alter table "Main".observations 
add column plant_label varchar(50);

alter table "Main".grow_cycles
add column is_control boolean default false;