import json

# Cache the haikus
_haikus_cache = None

def load_haikus():
    global _haikus_cache
    
    if _haikus_cache is None:
        with open("/sd/haiku.json", "r") as f:
            data = json.load(f)
            _haikus_cache = data["haikus"]
    
    return _haikus_cache

def get_current_haiku(rtc_time):
    """
    rtc_time: Tuple from machine.RTC().datetime()
    Format: (year, month, day, weekday, hour, minute, secon, subsecond)
    """
    
    haikus = load_haikus()
    
    hours = rtc_time[4]
    minutes = rtc_time[5]
    
    # Round to nearest 15-minute interval
    rounded_minute = (minutes // 15) * 15
    
    # Format time to match JSON format (HH:MM)
    time_str = f"{hours:02d}:{rounded_minute:02d}"
    
    for entry in haikus:
        if entry["time"] == time_str:
            return entry["haiku"]
    
    return None

# Get one haiku
def get_one_haiku(idx):
    haikus = load_haikus()
    return haikus[idx]["haiku"]

# Check if it's day or night
def is_day(rtc_time):
    hours = rtc_time[4]
    if 5 < hours < 20:
        return True
    else:
        return False