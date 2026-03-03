# Farm Data System
An open source farm management and data collection system built on PostgreSQL and Python. Built by a sustainable agriculture enthusiast and IT student who didn't like the capatlistic system farmers are put in and wanted real data to back up more sustainable farming practices.

---

## Why I Built This

I grow using natural farming principles - specifically KNF (Korean Natural Farming) and JADAM methods. The natural farming community has a documentation problem: a lot of results are shared anecdotally. Someone applies an input, a plant responds, and 
they assume it worked. That's cognitive bias, not evidence. But I want to be clear that I don't think KNF and JADAM are without merit - the founders of both systems are biologists who actually conducted studies when developing their inputs and methods. And Chris Trump's work documenting his macadamia nut farm in Hawaii - tracking exactly which inputs were necessary, at what ratios, and over multiple 
seasons - is what originally pulled me into this space. He collected real data and experimented methodically. That's the standard I want to hold myself to. The problem isn't that natural farming doesn't work, it's that most people in the community aren't documenting it rigorously enough. That's what this project is trying to fix.

At the same time, commercial agritech solutions for soil sensors, irrigation automation, and environment monitoring are expensive and lock you into their software ecosystem. I didn't want that.

I'm studying Python, databases, networking, and cybersecurity at USC, and I realized I could combine what I'm learning in school with what I actually care about - growing things to their maxiumn potential. So I built this system to:

- Scientifically document the effectiveness of natural farming inputs like  JMS, IMO, FAA, WCA, and fermented plant extracts with real controlled comparisons and measurable outcomes
- Track genetics, growing conditions, inputs applied, and yields in a structured database so I can query and analyze results across seasons
- Eventually replace expensive proprietary sensors with open source hardware built on Raspberry Pi

This is a long term project. The goal is to build up seasons worth of real data that either proves or disproves what natural farming practitioners claim their inputs do.

---

## What It Does Right Now

**Weather Data Collection**
- Automatically polls OpenWeatherMap API every 30 minutes
- Stores temperature, humidity, precipitation, wind, pressure, visibility, sunrise/sunset
- Data tied to exact coordinates for hyperlocal accuracy

**Farm Database**
- Tracks plots, crop genetics and varieties, and grow cycles
- Logs every input applied with dosage, dilution rate, and application method
- Flexible observation logging for height, yield, Brix, visual notes, or any metric
- Individual plant labeling within grow cycles for controlled comparisons
- Control group flagging for split plot experiments

**CLI Data Entry**
- Menu driven Python script for entering all data without writing SQL
- Add plots, crops, grow cycles, observations, and inputs from the terminal

---

## Current Tech Stack

- **Database:** PostgreSQL
- **Language:** Python 3
- **Libraries:** psycopg2, requests, python-dotenv
- **Weather:** OpenWeatherMap API
- **Tools:** DBeaver, Git

---

## What I'm Building Toward

- **Raspberry Pi integration** - run the database and scripts on a Pi so it doesn't depend on my personal machine
- **Open source sensors** - capacitive soil moisture, BME280 temp/humidity, TSL2591 lux sensors feeding directly into the database instead of buying proprietary systems
- **Automated irrigation** - relay controlled solenoid valves triggered by soil moisture thresholds or weather data
- **Indoor grow monitoring** - converting a shed into an indoor grow with full environment logging
- **Rainwater harvesting integration** - tracking rainfall capture and usage alongside irrigation data
- **Web interface** - eventually a simple Flask dashboard instead of CLI entry

---

## Setup

1. Clone the repo
2. Create a `.env` file in the scripts folder using `.env.example` as a template
3. Run `schema.sql` in your PostgreSQL database to create all tables
4. Install dependencies: `pip install psycopg2-binary requests python-dotenv`
5. Run `weather_poller.py` to start collecting weather data
6. Run `farm_entry.py` to start entering farm data

---

## Project Structure

```
/
├── schema.sql          # Database schema - run this first
├── weatherpoller.py    # Automated weather data collection
├── farm_entry.py       # CLI menu for data entry
├── .env.example        # Template for environment variables
├── .gitignore
└── DEVLOG.md           # Development journal and personal notes
```

---

## Philosophy

Most small scale farmers don't document enough. Most programmers don't farm or understand soil biology. This project sits at that intersection and tries to bring the rigor of data collection to practices that deserve more than anecdotal evidence. Everything here is open source because the point is to build something anyone can replicate, modify, and improve on their own land with their own data.

---

*Zone 7B | Columbia, SC | Started 2026*