# display resolution (supported: 64x48 and 128x64)
display_width = 64
display_height = 48

# choose whether the display uses i2c or spi
display_protocol = 'i2c'

# I2C pins for the SSD1306 display
sda = 123
scl = 123

# SPI pins for the SSD1306 display
dc = 123
reset = 123
cs = 123

# IP adress of the OctoPrint instance
ip = 'http://255.255.255.255/'

# Paste your API key here
# Instructions to get the key: docs.octoprint.org/en/master/api/general.html#authorization
# CORS needs to be enabled!
headers = {
    'X-Api-Key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
}