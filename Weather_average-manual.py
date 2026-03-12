#!/usr/bin/env/python3
#this tells the computer which program should run this file
import statistics
from statistics import mean
import psycopg2
from datetime import datetime
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
    SELECT (temp_f) FROM "Main".weather_data
    WHERE recorded_at >= NOW() - INTERVAL '7 days';
""")
#actually grabs results
rows = cur.fetchall()
print(rows)
close(conn, cur)

def calculate_average(numbers):
    if not numbers: # handles emplty list case to avoid division by zero
        return 0
    return sum(numbers) / len(numbers)


user_input = input("enter numbers seperated by commas: ")
x = user_input.split(",")


numbers = [float(num) for num in x]
average = statistics.mean(numbers)
print(average)


def main():
    

    if __name__ == "__main__":
        main()