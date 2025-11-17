#!/home/local/.config/waybar/scripts/venv/bin/python

import requests
from ics import Calendar
from datetime import datetime, timedelta
from dateutil import tz
import json
import time
#import arrow

ICAL_URL = "https://ical.example"
TIMEZONE = tz.gettz("Your/TimeZone") #e.g. Europe/Berlin

# Uncomment the following variable & function, uncomment the arrow import and switch the "now"-variable for checking if the script collects the right data

#sim_time = datetime(1999, 01, 01, 01, 01)

#def get_simulated_now():
#    global sim_time
#    timestamp = sim_time.strftime("%Y-%m-%dT%H:%M:%S") + "+02:00"
#    sim_time += timedelta(minutes=10)
#    return arrow.get(timestamp)

def get_current_event():
    try:
        text = requests.get(ICAL_URL, timeout=5).text
        cal = Calendar(text)
    except Exception as e:
        return None, f"error: {e}"

    now = datetime.now(TIMEZONE)
    #now = get_simulated_now()

    running = []

    for event in cal.events:

        start = event.begin
        end = event.end

        start_dt = start.datetime
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=TIMEZONE)

        end_dt = end.datetime
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=TIMEZONE)

        if start_dt <= now <= end_dt:
            running.append((event, start_dt, end_dt))

    if not running:
        return None, None

    return running[0], None


def make_bar(percent, length=20):
    filled = int(length * percent / 100)
    return "█" * filled + "░" * (length - filled)


while True:
    data, error = get_current_event()

    if error:
        print(json.dumps({}), flush=True)
        time.sleep(60)
        continue

    if data is None:
        print(json.dumps({
            "text": "",
            "percentage": 0
        }), flush=True)
        time.sleep(60)
        continue

    (event, start, end) = data

    now = datetime.now(TIMEZONE)
    #now = get_simulated_now()

    total = (end - start).total_seconds()
    passed = (now - start).total_seconds()
    percent = max(0, min(100, passed / total * 100))

    bar = make_bar(percent)

    text = f"{event.name} | {bar} {percent:.0f}%"

    print(json.dumps({
        "text": text,
        "percentage": percent
    }), flush=True)

    time.sleep(60)
