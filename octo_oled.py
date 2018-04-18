import machine
import ssd1306
import time
import urequests
import json
import octo_oled_config as config

# Takes a number of seconds and returns a string of format HH:mm:ss
def beautify_time(seconds):
    if seconds is None:
        return None

    # Hours
    res = ('0' if int(seconds/3600) < 10 else '')+str(int(seconds/3600))+':'
    seconds = seconds % 3600
    # Minutes
    res += ('0' if int(seconds/60) < 10 else '')+str(int(seconds/60))+':'
    seconds = seconds % 60
    # Seconds
    res += ('0' if seconds < 10 else '')+str(int(seconds))
    return res

# Returns filename, elapsed time, remaining time and progress of current print
def get_print_info():
    def req(url):
        while True: 
            try:
                return urequests.get(config.ip+url, headers=config.headers).content
            except requests.exceptions.RequestException as e:
                print(e)
            
    job_info = (req('api/job')).decode('utf-8')
    data = json.loads(job_info)

    if data['job']['file']['name'] is not None:
        return {
            'filename': data['job']['file']['name'],
            'elapsed': beautify_time(data['progress']['printTime']),
            'remaining': beautify_time(data['progress']['printTimeLeft']),
            'percentage': data['progress']['completion']
        }
    else:
        return None

# Sends the print information to the display
def display_print_info(info):
    oled.fill(0)

    # Show nothing on the display if there is no running print job
    if info is None:
        oled.show()
        return

    oled.text(info['filename'], 0, first_line)

    if info['percentage'] < 100:
        oled.text(info['elapsed'], 0, second_line)
        if info['remaining'] is not None:
            oled.text(info['remaining'], 0, third_line)
        if percentage_pos is not None:
            oled.text(str(int(info['percentage'])), percentage_pos[0], percentage_pos[1])

        # Progressbar
        for i in range(bar_margin_top, bar_margin_top + bar_height):
            for j in range(0, int((info['percentage']/100)*bar_length)):
                oled.pixel(j, i, 1)
    else:
        oled.text('Print', 0, second_line)
        oled.text('finished!', 0, third_line)

    oled.show()

# Initialize the display
if config.display_protocol == 'i2c':
    i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
    oled = ssd1306.SSD1306_I2C(
        config.display_width, config.display_height, i2c)

elif config.display_protocol == 'spi':
    spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)
    oled = ssd1306.SSD1306_SPI(config.display_width, config.display_height, spi, machine.Pin(
        config.dc), machine.Pin(config.reset), machine.Pin(config.cs))

# Configuring the output according to the resolution
if config.display_width == 64 and config.display_height == 48:
    first_line = 8
    second_line = 20
    third_line = 32
    percentage_pos = None
    bar_margin_top = 0
    bar_length = 64
    bar_height = 3
elif config.display_width == 128 and config.display_height == 64:
    first_line = 16
    second_line = 32
    third_line = 48
    percentage_pos = [112, 3]
    bar_margin_top = 3
    bar_length = 110
    bar_height = 6

while True:
    # Get and output the latest print job information every 15 seconds
    display_print_info(get_print_info())
    time.sleep(15.0)