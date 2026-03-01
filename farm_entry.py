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
    seed_source = prompt("Seed source", required=False)
    days_to_maturity = prompt_float("Days to maturity")
    perennial = prompt("Is this a perennial? (y/n)", default="n")
    notes = prompt("Notes", required=False)

    conn, cur = connect()
    cur.execute("""
        INSERT INTO crops (common_name, variety, species, seed_source, days_to_maturity, is_perennial, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (common_name, variety, species, seed_source, days_to_maturity, perennial.lower() == "y", notes))
    close(conn, cur)
    print(f"  Crop '{common_name} - {variety}' added successfully.")

# ── Add Grow Cycle ─────────────────────────────────────────

def add_grow_cycle():
    print("\n--- Add Grow Cycle ---")
    conn, cur = connect()

    print("\n  Select a plot:")
    plot_id = list_options(cur, "plots", "id", "name")
    if not plot_id:
        close(conn, cur)
        return

    print("\n  Select a crop:")
    crop_id = list_options(cur, "crops", "id", "common_name")
    if not crop_id:
        close(conn, cur)
        return

    start_date = prompt_date("Start date", required=True)
    is_control = prompt("Is this a control group? (y/n)", default="n")
    is_control = is_control.lower() == "y"
    transplant_date = prompt_date("Transplant date")
    expected_harvest = prompt_date("Expected harvest date")

    cur.execute("""
        INSERT INTO grow_cycles (plot_id, crop_id, status, start_date, is_control, transplant_date, expected_harvest_date)
        VALUES (%s, %s, 'active', %s, %s, %s, %s)
    """, (plot_id, crop_id, start_date, is_control, transplant_date, expected_harvest))
    close(conn, cur)
    print("  Grow cycle added successfully.")

# ── Log Observation ────────────────────────────────────────

def log_observation():
    print("\n--- Log Observation ---")
    conn, cur = connect()

    print("\n  Select a grow cycle:")
    cur.execute(f"""
        SELECT gc.id, c.common_name || ' - ' || p.name
        FROM "{SCHEMA}".grow_cycles gc
        JOIN "{SCHEMA}".crops c ON gc.crop_id = c.id
        JOIN "{SCHEMA}".plots p ON gc.plot_id = p.id
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

    print("\n  Observation types: visual, height_cm, yield_grams, brix, pest, disease, other")
    obs_type = prompt("Observation type")
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
        SELECT gc.id, c.common_name || ' - ' || p.name
        FROM "{SCHEMA}".grow_cycles gc
        JOIN "{SCHEMA}".crops c ON gc.crop_id = c.id
        JOIN "{SCHEMA}".plots p ON gc.plot_id = p.id
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
        print("  4. Log Observation")
        print("  5. Log Input Applied")
        print("  6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()

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
            print("\nGoodbye!\n")
            break
        else:
            print("  Invalid choice, please enter 1-6.")

if __name__ == "__main__":
    main()