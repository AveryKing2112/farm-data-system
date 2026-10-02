
CREATE TABLE "Main".cycle_plants (
    plant_id      SERIAL PRIMARY KEY,
    grow_cycle_id INT REFERENCES "Main".grow_cycles(grow_cycle_id),
    plot_name     TEXT, -- Keeping this simple to avoid needing a separate plots table if you don't have one
    row_num       INT,
    pos_num       INT,
    status        TEXT DEFAULT 'Alive' CHECK (status IN ('Alive', 'Dead', 'Harvested'))
);


CREATE INDEX idx_physical_location ON "Main".cycle_plants(plot_name, row_num, pos_num);

alter table "Main".observations
add column health_score int check (health_score between 1 and 10),
add column stress_factor text check (stress_factor in ('None', 'Weather', 'Pest', 'Nutrient', 'Water')),
add column action_taken text;



alter table "Main".observations
add column plant_id int references "Main".cycle_plants(plant_id);