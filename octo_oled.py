import machine
import ssd1306
import time
import urequests
import json
import config

# Takes a number of seconds and returns a string of format HH:mm:ss
def beautifyTime(seconds):
    # Hours
    res = str(("0" if int(seconds/3600)<10)+int(seconds/3600))+":"
    seconds = seconds%3600
    # Minutes
    res += str(("0" if int(seconds/60)<10)+int(seconds/60))+":"
    seconds = seconds%60
    # Seconds
    res += str(("0" if seconds<10)+int(seconds))
    return res

# Returns filename, elapsed time, remaining time and progress of current print job
def getPrintInfo():
    req = lambda url: urequests.get(config.ip+url,headers=config.headers).content
    job_info = (req('api/job')).decode('utf-8')
    data = json.loads(job_info)
    return [data["job"]["file"]["name"], beautifyTime(data["progress"]["printTime"]), beautifyTime(data["progress"]["printTimeLeft"]), data["progress"]["completion"]]

# Sends the print job information to the display
def displayPrintInfo(info):
    oled.fill(0)
    oled.text(info[0], 0, 16)
    oled.text(info[1],0,32)
    oled.text(info[2],0,48)
    oled.text("%",0,120)
    oled.text(str(int(info[3])),96,0)

    for i in range(3,9):
        for j in range(0,int((info[3]/100)*128)):
            oled.pixel(j,i,1)

    oled.show()


# Initialize the display
spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)
oled = ssd1306.SSD1306_SPI(128, 64, spi, machine.Pin(config.dc), machine.Pin(config.reset), machine.Pin(config.cs))

while True:
    # Get and output the information
    displayPrintInfo(getPrintInfo())
    time.sleep(10.0)