#!/usr/bin/env/python3
#this tells the computer which program should run this file
import statistics
from statistics import mean
import psycopg2
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path=r"c:\Users\bacca\AppData\Roaming\DBeaverData\workspace6\Farm database\Scripts\.env")
#---DBconfig---
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
    cur= conn.cursor()
    cur.execute(F'SET search_path TO "{SCHEMA}"')
    return conn, cur

def close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# Db query
conn, cur = connect()
cur.execute(""" 
    SELECT AVG(temp_f), AVG(humidity_percent), AVG(precip_inches), AVG(wind_mph), AVG(pressure_hpa) FROM "Main".weather_data
    WHERE recorded_at >= NOW() - INTERVAL '7 days';
""")
#actually grabs results
row = cur.fetchone()
avg_temp_f = float(row[0])
avg_humidity = float(row[1])
avg_precip = float(row[2])
avg_wind_mph = float(row[3])
avg_pressure_hpa = float(row[4])
week_end = date.today()
week_start = week_end - timedelta(days=7)
cur.execute("""
    INSERT INTO weather_summaries (week_start, week_end, avg_temp_F, avg_humidity, avg_wind_mph, total_precip_inches, avg_pressure_hpa)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (week_start, week_end, avg_temp_f, avg_humidity, avg_wind_mph, avg_precip, avg_pressure_hpa))
close(conn, cur)




def main():
    

    if __name__ == "__main__":
        main()