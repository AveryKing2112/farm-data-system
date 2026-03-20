import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"c:\Users\bacca\AppData\Roaming\DBeaverData\workspace6\Farm database\Scripts\.env")

# --- Config ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT"))
}
SCHEMA = os.getenv("DB_SCHEMA")

def connect():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(f'SET search_path TO "{SCHEMA}"')
    return conn, cur

def close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# ── Helpers ────────────────────────────────────────────────

def prompt(label, required=True, default=None):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        val = input(f"  {label}{suffix}: ").strip()
        if val == "" and default is not None:
            return default
        if val == "" and required:
            print("  This field is required.")
        else:
            return val if val != "" else None

def prompt_float(label, required=False):
    while True:
        val = input(f"  {label}: ").strip()
        if val == "" and not required:
            return None
        try:
            return float(val)
        except ValueError:
            print("  Please enter a number.")

def prompt_date(label, required=False):
    while True:
        val = input(f"  {label} (YYYY-MM-DD, or leave blank for today): ").strip()
        if val == "":
            return datetime.today().date() if required else None
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except ValueError:
            print("  Invalid date format. Use YYYY-MM-DD.")

def list_options(cur, table, id_col, display_col):
    cur.execute(f'SELECT {id_col}, {display_col} FROM "{SCHEMA}".{table}')
    rows = cur.fetchall()
    if not rows:
        print(f"  No {table} found. Please add one first.")
        return None
    print(f"\n  Available {table}:")
    for row in rows:
        print(f"    {row[0]}. {row[1]}")
    while True:
        val = input("  Enter ID: ").strip()
        try:
            val = int(val)
            if any(r[0] == val for r in rows):
                return val
            print("  Invalid ID.")
        except ValueError:
            print("  Please enter a number.")

# ── Add Plot ───────────────────────────────────────────────

def add_plot():
    print("\n--- Add Plot ---")
    name = prompt("Plot name")
    description = prompt("Description", required=False)
    area = prompt_float("Area (sq ft)")
    location_notes = prompt("Location notes (e.g. south facing, partial shade)", required=False)
    soil_notes = prompt("Soil notes", required=False)

    conn, cur = connect()
    cur.execute("""
        INSERT INTO plots (name, description, area_sqft, location_notes, soil_notes, is_active)
        VALUES (%s, %s, %s, %s, %s, TRUE)
    """, (name, description, area, location_notes, soil_notes))
    close(conn, cur)
    print(f"  Plot '{name}' added successfully.")

# ── Add Crop ───────────────────────────────────────────────

def add_crop():
    print("\n--- Add Crop ---")
    common_name = prompt("Common name (e.g. Basil)")
    variety = prompt("Variety (e.g. Scarlet Nantes)", required=False)
    species = prompt("Species (Latin name, e.g. Ocimum basilcum)", required=False)
    source_type = prompt("Source type (seed_packet/saved_seed/volunteer/wild/potted/trade)", required=False)
    seed_source = prompt("Seed source", required=False)
    days_to_maturity = prompt_float("Days to maturity")
    perennial = prompt("Is this a perennial? (y/n)", default="n")
    notes = prompt("Notes", required=False)

    conn, cur = connect()
    cur.execute("""
        INSERT INTO crops (common_name, variety, species, seed_source, days_to_maturity, is_perennial, source_type, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (common_name, variety, species, seed_source, days_to_maturity, perennial.lower() == "y", source_type, notes))
    close(conn, cur)
    print(f"  Crop '{common_name} - {variety}' added successfully.")

# ── Add Grow Cycle ─────────────────────────────────────────

def add_grow_cycle():
    print("\n--- Add Grow Cycle ---")
    conn, cur = connect()
    is_transplant_start = prompt("Is this starting indoors as a transplant? (y/n)", default="n")
    if is_transplant_start.lower() == "y":
        plot_id = None
    else:
        print("\n  Select a plot:")
        plot_id = list_options(cur, "plots", "plot_id", "name")
        if not plot_id:
            close(conn, cur)
            return

    print("\n  Select a crop:")
    crop_id = list_options(cur, "crops", "crop_id", "common_name")
    if not crop_id:
        close(conn, cur)
        return

    start_date = prompt_date("Start date( leave blank if unknown/wild)")
    is_control = prompt("Is this a control group? (y/n)", default="n")
    is_control = is_control.lower() == "y"
    sow_method = prompt("Sow method (transplant/direct/potted/vounteer/wild)", default="direct")
    if sow_method.lower() == "transplant":
        transplant_date = prompt_date("Transplant date")
        direct_sow_date = None
    elif sow_method.lower() == "direct":
        direct_sow_date = prompt_date("Direct sow date")
        transplant_date = None
    else:
        direct_sow_date = None
        transplant_date = None
    expected_harvest = prompt_date("Expected harvest date")

    cur.execute("""
        INSERT INTO grow_cycles (plot_id, crop_id, status, start_date, is_control, sow_method, transplant_date, direct_sow_date, expected_harvest_date)
        VALUES (%s, %s, 'active', %s, %s, %s, %s, %s, %s)
    """, (plot_id, crop_id, start_date, is_control, sow_method, transplant_date, direct_sow_date, expected_harvest))
    close(conn, cur)
    print("  Grow cycle added successfully.")

# ── Log Observation ────────────────────────────────────────

def log_observation():
    print("\n--- Log Observation ---")
    conn, cur = connect()

    print("\n  Select a grow cycle:")
    cur.execute(f"""
    SELECT gc.grow_cycle_id, c.common_name || ' - ' || COALESCE(p.name, 'Indoor Start'), gc.is_control
    FROM "{SCHEMA}".grow_cycles gc
    JOIN "{SCHEMA}".crops c ON gc.crop_id = c.crop_id
    LEFT JOIN "{SCHEMA}".plots p ON gc.plot_id = p.plot_id
    WHERE gc.status = 'active'
    """)
    rows = cur.fetchall()
    if not rows:
        print("  No active grow cycles found.")
        close(conn, cur)
        return
    for row in rows:
        control_label = " [CONTROL]" if row[2] else ""
        print(f"    {row[0]}. {row[1]}{control_label}")
    gc_id = int(input("  Enter ID: ").strip())

    print("\n  Observation types: germinated, sprouted, visual, height_cm, yield_grams, brix, pest, disease, other")
    obs_type = prompt("Observation type")
    if obs_type.lower() in ["germinated", "sprouted"]:
        value_text = "true"
        value_numeric = None
        notes = prompt("Notes (e.g which plant, any observations)", required=False)
        plant_label = prompt("Plant label (e.g plant 1, or leave blank for whole row)", required=False)
    else:
        value_numeric = prompt_float("Numeric value (if applicable)")
        value_text = prompt("Text observation", required=False)
        notes = prompt("Notes", required=False)
        plant_label = prompt("Plant label (e.g. plant 1, or leave blank for whole row)", required=False)
    
    cur.execute("""
        INSERT INTO observations (grow_cycle_id, observed_at, observation_type, value_numeric, value_text, plant_label, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (gc_id, datetime.now(), obs_type, value_numeric, value_text, plant_label, notes))
    close(conn, cur)
    print("  Observation logged successfully.")

# ── Log Input Applied ──────────────────────────────────────

def log_input():
    print("\n--- Log Input Applied ---")
    conn, cur = connect()

    print("\n  Select a grow cycle:")
    cur.execute(f"""
        SELECT gc.grow_cycle_id, c.common_name || ' - ' || COALESCE(p.name, 'Indoor Start')
        FROM "{SCHEMA}".grow_cycles gc
        JOIN "{SCHEMA}".crops c ON gc.crop_id = c.crop_id
        LEFT JOIN "{SCHEMA}".plots p ON gc.plot_id = p.plot_id
        WHERE gc.status = 'active'
    """)
    rows = cur.fetchall()
    if not rows:
        print("  No active grow cycles found.")
        close(conn, cur)
        return
    for row in rows:
        print(f"    {row[0]}. {row[1]}")
    gc_id = int(input("  Enter ID: ").strip())

    date_applied = prompt_date("Date applied", required=True)
    input_name = prompt("Input name (e.g. JADAM JMS)")
    input_amount = prompt_float("Input amount (ml)")
    water_amount = prompt_float("Water amount (ml)")
    dilution_rate = prompt("Dilution rate as text (e.g. 1:500)", required=False)
    method = prompt("Application method (e.g. foliar, soil drench)")
    notes = prompt("Notes", required=False)

    cur.execute("""
        INSERT INTO inputs_applied (grow_cycle_id, date_applied, input_name, input_amount_ml, water_amount_ml, dilution_rate, application_method, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (gc_id, date_applied, input_name, input_amount, water_amount, dilution_rate, method, notes))
    close(conn, cur)
    print("  Input logged successfully.")

# ── Add Ferments ──────────────────────────────────────

def add_ferment():
    print("\n--- Add Ferment ---")
    name = prompt("Ferment name (e.g. IMO Batch 1, LABS March)")
    ferment_type = prompt("Ferment type (e.g. IMO-1, LABS, FPJ, FFJ, FAA)")
    stage = prompt("Current stage (e.g. rice collection, milk addition, brown sugar)")
    started_at = prompt_date("Start date", required=True)
    vessel_size = prompt("Vessel size (e.g. 1 gallon jar, 5 gallon bucket)", required=False)
    notes = prompt("Notes (ingredients, ratios, location)", required=False)

    conn, cur = connect()
    cur.execute("""
        INSERT INTO "Main".ferments (name, ferment_type, stage, started_at, status, vessel_size, notes)
        VALUES (%s, %s, %s, %s, 'active', %s, %s)
    """, (name, ferment_type, stage, started_at, vessel_size, notes))
    close(conn, cur)
    print(f"  Ferment '{name}' added successfully.")

# ── Log Ferments ──────────────────────────────────────

def log_ferment():
    print("\n--- Log Ferment Observation ---")
    conn, cur = connect()

    cur.execute("""
        SELECT ferment_id, name || ' - ' || ferment_type || ' (' || stage || ')'
        FROM "Main".ferments
        WHERE status = 'active'
    """)
    rows = cur.fetchall()
    if not rows:
        print("  No active ferments found.")
        close(conn, cur)
        return
    print("\n  Active ferments:")
    for row in rows:
        print(f"    {row[0]}. {row[1]}")
    ferment_id = int(input("  Enter ID: ").strip())

    stage = prompt("Current stage (leave blank if unchanged)", required=False)
    temp_f = prompt_float("Temperature (F, if applicable)")
    action_taken = prompt("Action taken (e.g. turned, added milk, strained)", required=False)
    observations = prompt("Observations (smell, color, texture, mycelium coverage)", required=False)
    notes = prompt("Notes", required=False)

    cur.execute("""
        INSERT INTO "Main".ferment_logs (ferment_id, logged_at, stage, temp_f, action_taken, observations, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (ferment_id, datetime.now(), stage, temp_f, action_taken, observations, notes))

    if stage:
        cur.execute("""
            UPDATE "Main".ferments SET stage = %s WHERE ferment_id = %s
        """, (stage, ferment_id))

    close(conn, cur)
    print("  Ferment log entry saved.")

    # ── Initialize Physical Grid ─────────────────────────────────

def initialize_grid():
    print("\n--- Initialize Physical Grid ---")
    conn, cur = connect()

    # 1. Select the Grow Cycle (borrowing your exact logic)
    print("\n  Select a grow cycle:")
    cur.execute(f"""
        SELECT gc.grow_cycle_id, c.common_name || ' - ' || COALESCE(p.name, 'Indoor Start')
        FROM "{SCHEMA}".grow_cycles gc
        JOIN "{SCHEMA}".crops c ON gc.crop_id = c.crop_id
        LEFT JOIN "{SCHEMA}".plots p ON gc.plot_id = p.plot_id
        WHERE gc.status = 'active'
    """)
    rows = cur.fetchall()
    if not rows:
        print("  No active grow cycles found.")
        close(conn, cur)
        return
    for row in rows:
        print(f"    {row[0]}. {row[1]}")
    
    try:
        gc_id = int(input("  Enter ID: ").strip())
    except ValueError:
        print("  Invalid ID.")
        close(conn, cur)
        return

    # 2. Get Grid Dimensions
    num_rows = int(prompt_float("How many rows?", required=True))
    plants_per_row = int(prompt_float("How many plants per row?", required=True))

    print(f"\n  Generating {num_rows * plants_per_row} individual plant records...")

    # 3. Insert into the cycle_plants table
    insert_query = f"""
        INSERT INTO "{SCHEMA}".cycle_plants (grow_cycle_id, row_num, pos_num, status)
        VALUES (%s, %s, %s, 'Alive')
    """
    for row in range(1, num_rows + 1):
        for pos in range(1, plants_per_row + 1):
            cur.execute(insert_query, (gc_id, row, pos))

    close(conn, cur)
    print("  Grid initialized successfully!")

# ── Log Specific Plant Observation ───────────────────────────

def log_specific_plant():
    print("\n--- Log Specific Plant Observation ---")
    conn, cur = connect()

    # 1. Select the Grow Cycle
    print("\n  Select a grow cycle:")
    cur.execute(f"""
        SELECT gc.grow_cycle_id, c.common_name || ' - ' || COALESCE(p.name, 'Indoor Start')
        FROM "{SCHEMA}".grow_cycles gc
        JOIN "{SCHEMA}".crops c ON gc.crop_id = c.crop_id
        LEFT JOIN "{SCHEMA}".plots p ON gc.plot_id = p.plot_id
        WHERE gc.status = 'active'
    """)
    rows = cur.fetchall()
    if not rows:
        print("  No active grow cycles found.")
        close(conn, cur)
        return
    for row in rows:
        print(f"    {row[0]}. {row[1]}")
        
    try:
        gc_id = int(input("  Enter ID: ").strip())
    except ValueError:
        print("  Invalid ID.")
        close(conn, cur)
        return

    # 2. Find the coordinates
    row_num = int(prompt_float("Row #", required=True))
    pos_num = int(prompt_float("Position #", required=True))

    # 3. Lookup the exact plant_id
    cur.execute(f"""
        SELECT plant_id, status FROM "{SCHEMA}".cycle_plants 
        WHERE grow_cycle_id = %s AND row_num = %s AND pos_num = %s
    """, (gc_id, row_num, pos_num))
    
    result = cur.fetchone()
    if not result:
        print("  Error: No plant found at those coordinates. Did you run 'Initialize Grid' for this cycle?")
        close(conn, cur)
        return
        
    plant_id = result[0]

    # 4. Gather Metrics
    health = int(prompt_float("Health Score (1-10)", required=True))
    
    print("\n  Stress Factors: [1] None  [2] Weather  [3] Pest  [4] Nutrient  [5] Water")
    stress_choice = prompt("Select Stress (1-5)", default="1")
    stress_map = {'1':'None', '2':'Weather', '3':'Pest', '4':'Nutrient', '5':'Water'}
    stress = stress_map.get(stress_choice, 'None')
    
    action = prompt("Action Taken (e.g. Sprayed JLF, None)", default="None")
    notes = prompt("Detailed Notes (e.g. True leaves emerged)", required=False)

    # 5. Save to the existing observations table
    cur.execute(f"""
        INSERT INTO "{SCHEMA}".observations 
        (grow_cycle_id, plant_id, observed_at, observation_type, health_score, stress_factor, action_taken, notes)
        VALUES (%s, %s, %s, 'specific_plant', %s, %s, %s, %s)
    """, (gc_id, plant_id, datetime.now(), health, stress, action, notes))

    close(conn, cur)
    print(f"  Observation logged successfully for Plant ID {plant_id}.")

# ── Main Menu ──────────────────────────────────────────────

# ── Main Menu ──────────────────────────────────────────────

def main():
    print("\n============================")
    print("   Farm Data Entry System   ")
    print("============================")
    while True:
        print("\nWhat would you like to do?")
        print("  1. Add Plot")
        print("  2. Add Crop")
        print("  3. Add Grow Cycle")
        print("  4. Log Observation (General)")
        print("  5. Log Input Applied")
        print("  6. Add Ferment")
        print("  7. Log Ferment Observation")
        print("  8. Initialize Physical Grid")
        print("  9. Log Specific Plant (Grid Coordinates)")
        print("  10. Exit")

        choice = input("\nEnter choice (1-10): ").strip()

        if choice == "1":
            add_plot()
        elif choice == "2":
            add_crop()
        elif choice == "3":
            add_grow_cycle()
        elif choice == "4":
            log_observation()
        elif choice == "5":
            log_input()
        elif choice == "6":
            add_ferment()
        elif choice == "7":
            log_ferment()
        elif choice == "8":
            initialize_grid()
        elif choice == "9":
            log_specific_plant()
        elif choice == "10":
            print("\nGoodbye!\n")
            break
        else:
            print("  Invalid choice, please enter 1-10.")

if __name__ == "__main__":
    main()