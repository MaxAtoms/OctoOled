import machine
import ssd1306
import time
import urequests
import json
import octo_oled_config as config

# Takes a number of seconds and returns a string of format HH:mm:ss
def beautifyTime(seconds):
    if seconds is None:
        return None
    
    # Hours
    res = ('0' if int(seconds/3600)<10 else '')+str(int(seconds/3600))+':'
    seconds = seconds%3600
    # Minutes
    res += ('0' if int(seconds/60)<10 else '')+str(int(seconds/60))+':'
    seconds = seconds%60
    # Seconds
    res += ('0' if seconds<10 else '')+str(int(seconds))
    return res

# Returns filename, elapsed time, remaining time and progress of current print
def getPrintInfo():
    req = lambda url: urequests.get(config.ip+url,headers=config.headers).content
    job_info = (req('api/job')).decode('utf-8')
    data = json.loads(job_info)
    
    if data['job']['file']['name'] is not None:
        return { 
            'filename': data['job']['file']['name'],
            'elapsed': beautifyTime(data['progress']['printTime']),
            'remaining': beautifyTime(data['progress']['printTimeLeft']),
            'percentage': data['progress']['completion'] 
        }
    else:
        return None

# Sends the print information to the display
def displayPrintInfo(info):
    oled.fill(0)

    # Show nothing on the display if there is no running print job
    if info is None:
        oled.show()
        return

    oled.text(info['filename'], 0, 16)

    if info['percentage'] < 100:
        oled.text(info['elapsed'],0,32)
        if info['remaining'] is not None:
            oled.text(info['remaining'],0,48)
        oled.text(str(int(info['percentage'])),112,3)
    
        # Progressbar
        for i in range(3,9):
            for j in range(0,int((info['percentage']/100)*110)):
                oled.pixel(j,i,1)
    else:
        oled.text('Print',0,32)
        oled.text('finished!',0,48)

    oled.show()


# Initialize the display
spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)
oled = ssd1306.SSD1306_SPI(128, 64, spi, machine.Pin(config.dc), machine.Pin(config.reset), machine.Pin(config.cs))

while True:
    # Get and output the information
    displayPrintInfo(getPrintInfo())
    time.sleep(15.0)