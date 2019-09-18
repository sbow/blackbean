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
	
def RelayOn(self):
	relay.On()

def RelayOff(self);
	relay.Off()

def LedColor(self, rgb=(1,1,1))
	led.value = rgb

def DbConnect(self):
	con = sqlite3.connect(DATABASE) 
	cursorObj = con.cursor()
