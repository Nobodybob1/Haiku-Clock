import inky_frame
from machine import RTC
import network
import time
import ntptime
from secrets import WIFI_SSID, WIFI_PASSWORD, TIMEZONE_OFFSET

def is_time_synced():
    rtc = RTC()
    current = rtc.datetime()
    year = current[0]
    
    if year < 2026:
        return False
    return True

def sync_time_from_internet():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    try:
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        
        if wlan.isconnected():
            # Try multiple NTP servers
            ntp_servers = [
                "pool.ntp.org",      # Default
                "time.google.com",   # Google's NTP
                "time.cloudflare.com", # Cloudflare
                "time.windows.com",  # Microsoft
                "europe.pool.ntp.org" # European pool
            ]
            synced = False
            
            for ntp_host in ntp_servers:
                try:
                    print(f"   Trying {ntp_host}...")
                    ntptime.host = ntp_host
                    ntptime.settime()
                    time.sleep(1)
                    synced = True
                    print(f"   ✅ Success with {ntp_host}")
                    break
                except OSError as e:
                    print(f"   ❌ {ntp_host} failed: {e}")
                    continue
            
            if not synced:
                print("❌ All NTP servers failed!")
                wlan.disconnect()
                wlan.active(False)
                return False
            
            rtc = RTC()
            utc_time = rtc.datetime()
            print(f"   UTC time: {utc_time[4]:02d}:{utc_time[5]:02d}:{utc_time[6]:02d}")
            
            # Apply timezone offset
            year, month, day, weekday, hour, minute, second, subsecond = utc_time
            
            # Add timezone offset to hour
            hour += TIMEZONE_OFFSET
            
            # Handle day rollover
            if hour >= 24:
                hour -= 24
                day += 1  
            elif hour < 0:
                hour += 24
                day -= 1
            
            # Update RTC with local time
            local_time = (year, month, day, weekday, hour, minute, second, subsecond)
            rtc.datetime(local_time)
            
            # Save to hardware clock
            inky_frame.pico_rtc_to_pcf()
            time.sleep(2)
            
            wlan.disconnect()
            wlan.active(False)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Sync failed: {e}")
        import sys
        sys.print_exception(e)
        return False
    finally:
        wlan.active(False)