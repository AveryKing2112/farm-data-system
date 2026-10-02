create or replace view "Main".v_plant_directory as
select
	p.plant_id,
	pl.name as plot_name,
	p.row_num,
	p.pos_num,
	p.status,
	gc.grow_cycle_id,
	gc.start_date,
	c.common_name,
	c.variety
from "Main".cycle_plants p
join "Main".grow_cycles gc on p.grow_cycle_id = gc.grow_cycle_id
join "Main".crops c on gc.crop_id = c.crop_id
left join "Main".plots pl on gc.plot_id = pl.plot_id;