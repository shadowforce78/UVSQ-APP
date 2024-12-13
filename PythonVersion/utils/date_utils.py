
from datetime import datetime, timedelta

def get_monday_date():
    today = datetime.now()
    return today - timedelta(days=today.weekday())

def get_week_dates(reference_date):
    monday = reference_date - timedelta(days=reference_date.weekday())
    friday = monday + timedelta(days=4)
    return monday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d")

def format_week_display(start_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + timedelta(days=4)
    return f"Semaine du {start.strftime('%d/%m/%Y')} au {end.strftime('%d/%m/%Y')}"

def normalize_time(time_str):
    hour = int(time_str.split(":")[0])
    return f"{hour:02d}:00"

def format_time(time_str):
    return normalize_time(time_str.strip().split()[1])

def get_day_from_date(date_str):
    try:
        return date_str.strip().split()[0].split("/")[0]
    except:
        return None

def get_nearest_time_slot(time_str):
    hour, minute = map(int, time_str.split(":"))
    minute = round(minute / 15) * 15
    if minute == 60:
        hour += 1
        minute = 0
    return f"{hour:02d}:{minute:02d}"