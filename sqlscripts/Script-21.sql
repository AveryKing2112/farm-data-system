ALTER TABLE "Main".cycle_plants 
ADD COLUMN plot_id INT REFERENCES "Main".plots(plot_id);


ALTER TABLE "Main".cycle_plants 
DROP COLUMN plot_name;




update "Main".cycle_plants
set plot_id = 2
where grow_cycle_id = 16

INSERT INTO "Main".observations (grow_cycle_id, plant_id, observed_at, observation_type, notes)
SELECT 
    cp.grow_cycle_id, 
    cp.plant_id, 
    CURRENT_TIMESTAMP, 
    'group_update', 
    'Winter radishes established true leaves after freeze.'
FROM "Main".cycle_plants cp
JOIN "Main".grow_cycles gc ON cp.grow_cycle_id = gc.grow_cycle_id
JOIN "Main".plots p ON cp.plot_id = p.plot_id
WHERE p.name = 'Bed B' 
  AND gc.crop_id = 7;