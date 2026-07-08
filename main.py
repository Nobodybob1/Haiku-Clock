import inky_frame
from display import day_picture, night_picture
from haiku_data import get_current_haiku, get_one_haiku, is_day
from machine import RTC
from sd_card import mount_sd_card
from sync_time import is_time_synced, sync_time_from_internet
import time

print("=== HAIKU CLOCK DEBUG ===\n")
SLEEP_MINUTES = 15

if mount_sd_card():
    time.sleep(1)
    
    # Read from hardware clock
    inky_frame.pcf_to_pico_rtc()
    time.sleep(0.5)
    
    # Check if needs sync
    if not is_time_synced():
        if not sync_time_from_internet():
            print("⚠️ Sync failed - using default time")
    
    # Current time
    rtc = RTC()
    current_time = rtc.datetime()
    
    # Get haiku
    print(f"4. Looking for haiku at {current_time[4]:02d}:{current_time[5]:02d}...")
    haiku = get_current_haiku(current_time)
    print(f"   Found: {haiku}\n")
    
    # Check day/night
    print(f"5. Is it daytime? {is_day(current_time)}")
    print(f"   (Hour is {current_time[4]}, day is 5 < hour < 20)\n")
    
    # Display
    print("6. Rendering display...")
    if is_day(current_time):
        print("   Using DAY picture")
        day_picture(haiku)
    else:
        print("   Using NIGHT picture")
        night_picture(haiku)
    
    print("\n✓ Done!")
    
    # Sleep
    
    # Calculate correct time for sleep
    SLEEP_MINUTES = (current_time[5] // 15 + 1) * 15 - current_time[5]
    inky_frame.sleep_for(SLEEP_MINUTES)
else:
    print("❌ SD card mount failed!")
    inky_frame.sleep_for(SLEEP_MINUTES)

