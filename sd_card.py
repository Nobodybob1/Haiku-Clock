import os
from machine import SPI, Pin

def mount_sd_card():
    try:
        import sdcard
        spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
        sd = sdcard.SDCard(spi, Pin(22))
        os.mount(sd, "/sd")
        print("SD card mounted successfully")
        return True
    except Exception as e:
        print(f"Failed to mount SD card: {e}")
        return False
        