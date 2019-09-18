#   blackbean.py
#  
#   An office coffee machine controller
#
#   https://github.com/sbow/blackbean
#   
#   v0.1
#   2019/09/12
#   Initial framework of controller

#Coffee Maker Database Setup
import sqlite3
DATABASE = 'blackbean.db'
con = None
cursorObj = None

#TFT Display Setup - ST7789 Adafruit 240x240 1.54" SPI
from PIL import Image
import Adafruit_ST7789 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
PIN_DC = 24 
PIN_RST = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = None

# Solid State Relay and RGB LED Setup
from gpiozero import RGBLED, LED
from time import sleep

# Solid State Relay Setup - Omron
PIN_RELAY = 26
relay = None

# RGB LED Setup - Note CA LED: values reversed, led.On() turns OFF led
PIN_RED   = 5
PIN_GREEN = 6
PIN_BLUE  = 4
C_GREEN = (1,0.5,1)
C_TEAL  = (1,0.8,0.5)
T_PULSE = 0.5
led = None

def __init__(self):
	led = RGBLED(PIN_RED, PIN_GREEN, PIN_BLUE)
	relay = LED(PIN_RELAY)

def LedDemo(self):
	led.pulse(T_PULSE, T_PULSE, C_TEAL, C_GREEN)
	sleep(10)

def RelayDemo(self):
	relay.blink(1)
	sleep(10)
	
def TftDemo(self):
	# Create TFT LCD display class.
	disp = TFT.ST7789(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

	# Initialize display.
	disp.begin()

	# Clear the display to a red background.
	# Can pass any tuple of red, green, blue values (from 0 to 255 each).
	disp.clear((255, 0, 0))

	# Get a PIL Draw object to start drawing on the display buffer.
	draw = disp.draw()

	# Draw a cyan triangle with a black outline.
	draw.polygon([(10, 275), (110, 240), (110, 310)], outline=(0,0,0), fill=(0,255,255))

	# Load default font.
	font = ImageFont.load_default()	
	
	# Write two lines of white text on the buffer, rotated 90 degrees counter clockwise.
	draw_rotated_text(disp.buffer, 'Hello World!', (150, 120), 90, font, fill=(255,255,255))
	draw_rotated_text(disp.buffer, 'This is a line of text.', (170, 90), 90, font, fill=(255,255,255))

	# Write buffer to display hardware, must be called to make things visible on the
	# display!
	disp.display()	

def RelayOn(self):
	relay.On()

def RelayOff(self);
	relay.Off()

def LedColor(self, rgb=(1,1,1))
	led.value = rgb

def DbConnect(self):
	con = sqlite3.connect(DATABASE) 
	cursorObj = con.cursor()

# Define a function to create rotated text.  Unfortunately PIL doesn't have good
# native support for rotated fonts, but this function can be used to make a
# text image and rotate it so it's easy to paste in the buffer.
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)
