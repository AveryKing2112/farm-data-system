import psycopg2
import requests 
from datetime import datetime
import time
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"c:\Users\bacca\AppData\Roaming\DBeaverData\workspace6\Farm database\Scripts\.env")


API_KEY = os.getenv("OWM_API_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT"))
}
SCHEMA = os.getenv("DB_SCHEMA")

POLL_INTERVAL_MINUTES = 30

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=imperial"
    response = requests.get(url)
    data = response.json()
    return {
        "recorded_at": datetime.now(),
        "temp_f": data["main"]["temp"],
        "temp_min_f": data["main"]["temp_min"],
        "temp_max_f": data["main"]["temp_max"],
        "feels_like_f": data["main"]["feels_like"],
        "humidity_percent": data["main"]["humidity"],
        "pressure_hpa": data["main"]["pressure"],
        "sea_level_hpa": data["main"].get("sea_level"),
        "ground_level_hpa": data["main"].get("grnd_level"),
        "visibility_m": data.get("visibility"),
        "precip_inches": data.get("rain", {}).get("1h", 0),
        "wind_mph": data["wind"]["speed"],
        "conditions": data["weather"][0]["description"],
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"])
    }

def insert_weather(weather):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO "Main".weather_data (
            recorded_at, temp_f, temp_min_f, temp_max_f, feels_like_f,
            humidity_percent, pressure_hpa, sea_level_hpa, ground_level_hpa,
            visibility_m, precip_inches, wind_mph, conditions, sunrise, sunset
        )
        VALUES (
            %(recorded_at)s, %(temp_f)s, %(temp_min_f)s, %(temp_max_f)s, %(feels_like_f)s,
            %(humidity_percent)s, %(pressure_hpa)s, %(sea_level_hpa)s, %(ground_level_hpa)s,
            %(visibility_m)s, %(precip_inches)s, %(wind_mph)s, %(conditions)s, %(sunrise)s, %(sunset)s
        )
    """, weather)
    conn.commit()
    cur.close()
    conn.close()

def main():
    print("Weather poller started...")
    while True:
        try:
            weather = get_weather()
            insert_weather(weather)
            print(f"Logged weather at {weather['recorded_at']}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(POLL_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()