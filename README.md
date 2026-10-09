# Farm Data System
An open source farm management and data collection system built on PostgreSQL and Python. Built by a sustainable agriculture enthusiast and IT student who wanted real data to further prove sustainable farming practices are obtainable and beneficial.

---

## Why I Built This

I grow using natural farming principles, specifically KNF (Korean Natural Farming) and JADAM methods. I believe that with more research, natural farming has a lot more to offer. Many growers I've followed online, myself included, have come to the same conclusion: most of the core natural farming inputs could be made more efficient and cost-effective, or improved on entirely.

Dr. Cho Han-Kyu, the founder of KNF, did most of his research from the 1960s through the 1990s. We know much more about soil and ecosystems today than we did when these methods were first developed. What originally pulled me into this was Chris Trump's work documenting his macadamia nut farm in Hawaii, where he tracked exactly which inputs were necessary, at what ratios, and over multiple seasons. He collected real data and experimented methodically. That's the standard I want to hold myself to. The problem isn't that natural farming doesn't work. It's that there arent enough people in the community documenting and experimenting rigorously enough, and that's what this project is trying to change.

At the same time, commercial agritech solutions for soil sensors, irrigation automation, and environment monitoring can be expensive and tend to lock you into their software ecosystem. I didn't want to spend that kind of money or be locked in.

Studying IT made me realize I could combine what I'm learning in school with what I actually care about: expanding soil microbiology and growing things to their maximum potential. So I built this system to:

- Scientifically document the effectiveness of natural farming and JADAM inputs like JLF, LAB, JMS, IMO, FAA, WCA, FPJ, FFJ, and FPE with controlled comparisons and measurable outcomes
- Track genetics, growing conditions, climate, inputs, yields, and more in a structured database so I can analyze results across seasons
- Eventually incorporate open source hardware built on Raspberry Pi and ESP32

This is a long-term project. The goal is to build up seasons' worth of data.

---

## What It Does Right Now

**Weather Data Collection**
- Automatically polls the OpenWeatherMap API every 30 minutes
- Stores temperature, humidity, precipitation, wind, pressure, visibility, and sunrise/sunset
- Data is tied to exact coordinates for hyperlocal accuracy

**Farm Database**
- Tracks plots, crop genetics, varieties, and grow cycles
- Logs every input applied with dosage, dilution rate, and application method
- Flexible observation logging for height, yield, Brix, visual notes, or any other metric
- Individual plant labeling within grow cycles for controlled comparisons
- Control group flagging for split-plot experiments
- Fermentation tracking for input batches, with stage-by-stage logs

**CLI Data Entry**
- Menu-driven Python script for entering data
- Add plots, crops, grow cycles, observations, and inputs from the terminal

---

## Current Tech Stack

- **Database:** PostgreSQL with the TimescaleDB extension (for time-series weather data)
- **Language:** Python 3
- **Libraries:** psycopg2, requests, python-dotenv
- **Weather:** OpenWeatherMap API
- **Tools:** DBeaver, Git

---

## What I'm Building Toward

- **Raspberry Pi integration:** run the database and scripts on a Pi so it doesn't depend on my personal machine
- **Open source sensors:** capacitive soil moisture, SHT45 temperature/humidity, and TSL2591 light sensors feeding directly into the database instead of buying proprietary systems
- **Automated irrigation:** relay-controlled solenoid valves triggered by soil moisture thresholds or weather data
- **Indoor grow monitoring:** converting a shed into an indoor grow with full environment logging
- **Rainwater harvesting integration:** tracking rainfall capture and usage alongside irrigation data
- **Web interface:** a simple Flask dashboard to replace CLI entry

---

## Setup

1. Clone the repo
2. Install PostgreSQL and the [TimescaleDB](https://docs.timescale.com/) extension
3. Run `FarmSchema.sql` in your PostgreSQL database to create all tables
4. Create a `.env` file in the scripts folder using `.env.example` as a template
5. Install dependencies: `pip install psycopg2-binary requests python-dotenv`
6. Run `weatherpoller.py` to start collecting weather data
7. Run `farm_entry.py` to start entering farm data

---

## Project Structure

```
/
├── FarmSchema.sql      # Database schema - run this first
├── weatherpoller.py    # Automated weather data collection
├── farm_entry.py       # CLI menu for data entry
├── .env.example        # Template for environment variables
├── .gitignore
└── DEVLOG.md           # Development journal and personal notes
```

---

## Philosophy

In my opinion, most small-scale farmers don't document enough, and most programmers don't farm or study soil biology. This project sits at that intersection and tries to bring the rigor of data collection to an area that deserves more attention. Everything here is open source because the point is to build something anyone can replicate, modify, and improve on their own land with their own data.

---

*Zone 7B | Columbia, SC | Started 2026*
