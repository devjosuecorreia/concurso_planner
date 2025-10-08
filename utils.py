import os
import datetime as dt

def ensure_dirs():
    up = os.environ.get("UPLOADS_DIR") or os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(up, exist_ok=True)

def today():
    return dt.date.today()

def start_of_week(d: dt.date):
    # considera segunda como início
    return d - dt.timedelta(days=d.weekday())

def end_of_week(d: dt.date):
    return start_of_week(d) + dt.timedelta(days=6)

def human_duration(total_minutes: int):
    h = total_minutes // 60
    m = total_minutes % 60
    if h > 0:
        return f"{h}h {m}min"
    return f"{m}min"
