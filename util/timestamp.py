from datetime import datetime
from dateutil import parser
from zoneinfo import ZoneInfo

def generate_timestamp():
    time = datetime.now(ZoneInfo("Asia/Seoul"))
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def generate_isotimestamp():
    return datetime.now(ZoneInfo("Asia/Seoul")).isoformat()

def convert_iso_to_general(iso_timestamp):
    time = parser.parse(iso_timestamp)
    return time.strftime("%Y-%m-%dT%H:%M:%S")