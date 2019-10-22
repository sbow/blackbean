#   blackbean.py
#  
#   An office coffee machine controller
#
#   https://github.com/sbow/blackbean
#   
#   v0.1
#   2019/09/12
#   Initial framework of controller

import bbsql # sqlite database interface class
import bbscan # PN532 RFID interface class
import bbenc # encryption class
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_ST7789 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import textwrap
from gpiozero import RGBLED, LED
from time import sleep

class bbrun:
    # BBEnc encryption object
    bbenc = None

    # PN532 Scanner object
    bbsc = None # PN532 object

    #Coffee Maker Database Setup
    DATABASE = r'blackbean.db'
    DATAPATH = r''
    bbdb = None # sqlite object
    
    #TFT Display Setup - ST7789 Adafruit 240x240 1.54" SPI
    PIN_DC = 24 
    PIN_RST = 23
    SPI_PORT = 0
    SPI_DEVICE = 0
    disp = None

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

    # Last scan array - to be used by functions in bbrun
    lastscan = None

    def __init__(self):
    	self.led = RGBLED(self.PIN_RED, self.PIN_GREEN, self.PIN_BLUE)
        self.led.value = (1,1,0)

    	self.relay = LED(self.PIN_RELAY)
    
    	# Create TFT LCD display class.
    	self.disp = TFT.ST7789(self.PIN_DC, rst=self.PIN_RST, \
                            spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, \
                                           max_speed_hz=64000000))
    	# Initialize display.
    	self.disp.begin()
    	# Clear the display to a red background.
    	# Can pass any tuple of blue, green, red values (from 0 to 255 each).
    	self.disp.clear((255, 0, 0))
    
        # Initialize blackbean database class
        self.bbdb = bbsql.bbdb(self.DATAPATH, self.DATABASE)

        # Initialize PN532 RFID class
        self.bbsc = bbscan.bbscan()
        print(self.bbsc.resp)

        # Initialize encryption class
        self.bbenc = bbenc.bbenc()
        self.bbenc.load_public()
        print(self.bbenc.resp)

    def LedDemo(self):
    	self.led.pulse(self.T_PULSE, self.T_PULSE, self.C_TEAL, self.C_GREEN)
    	sleep(10)
    
    def RelayDemo(self):
    	self.relay.blink(1)
    	sleep(10)
    	
    def TftDemo(self):
    	# Get a PIL Draw object to start drawing on the display buffer.
    	draw = self.disp.draw()
    
    	# Draw a cyan triangle with a black outline.
    	draw.polygon(   [(10, 275), (110, 240), (110, 310)], outline=(0,0,0), \
                        fill=(0,255,255))
    
    	# Load default font.
    	font = ImageFont.load_default()	
    	
    	# Write two lines of white text on the buffer, rotated 90 degrees counter clockwise.
    	self.DrawRotatedText(self.disp.buffer, 'Hello World!', (150, 120), \
                            90, font, fill=(255,255,255))
    	self.DrawRotatedText(self.disp.buffer, 'This is a line of text.', \
                            (170, 90), 90, font, fill=(255,255,255))
    
    	# Write buffer to display hardware, must be called to make things visible on the
    	# display!
    	self.disp.display()	
    
    def RelayOn(self):
    	self.relay.on()
    
    def RelayOff(self):
    	self.relay.off()
    
    def LedColor(self, rgb=(1,1,1)):
    	self.led.value = rgb
    
    # Define a function to create rotated text.  Unfortunately PIL doesn't have good
    # native support for rotated fonts, but this function can be used to make a
    # text image and rotate it so it's easy to paste in the buffer.
    def DrawRotatedText(self, image, text, position, angle, font, \
                          fill=(255,255,255)):
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

    # Display Fortune
    def DrawFortune(self, fortune):
        font = ImageFont.truetype('Momt___.ttf',22)
        angle = 0
        self.disp.buffer.paste((0,0,0), (0,0,240,240))
        length = len(fortune) # number of characters
        CHARLINEMAX = 16
        LINEMAX = 10
        LINESPACE = 20
        XSTART = 10
        YSTART = 10
        FILL = (255,255,255)
        lines = textwrap.wrap(fortune, CHARLINEMAX, break_long_words=False)
        x = XSTART
        y = YSTART
        for line in lines:
            self.DrawRotatedText( \
                self.disp.buffer, line, (x,y), angle, font, fill=FILL)
            y = y + LINESPACE
        self.disp.display()

    # Display Image
    def DisplayImage(self, dirname, imagename):
        image = Image.open(dirname+"/"+imagename) #assume 240x240
        self.disp.display(image) # assume angle 0

    # Display Homescreen
    def DrawHome(self):
        font = ImageFont.truetype('Play With Fire.ttf',42)
        fonttwo = ImageFont.truetype('Momt___.ttf',22)
        angle = 0
        self.disp.buffer.paste((0,0,0), (0, 0, 240, 240))
        self.DrawRotatedText( \
                self.disp.buffer, 'Coffee', (10, 10), angle, font, fill=(255,255,255))
        self.DrawRotatedText(\
                self.disp.buffer, 'Club', (10, 70), angle, font, fill=(255,255,255))
        self.DrawRotatedText(\
                self.disp.buffer, 'Scan Badge', (10, 180), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'Get Coffee', (10, 200), angle, fonttwo, fill=(230,230,230))
        self.disp.display()

    # Display Brewscreen
    def DrawBrew(self):
        font = ImageFont.truetype('Play With Fire.ttf',42)
        fonttwo = ImageFont.truetype('Momt___.ttf',22)
        angle = 0
        self.disp.buffer.paste((0,0,0), (0, 0, 240, 240))
        self.DrawRotatedText( \
                self.disp.buffer, 'Brewing', (10, 10), angle, font, fill=(0,255,0))
        self.DrawRotatedText(\
                self.disp.buffer, 'Yum yum!', (10, 90), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'Issues?', (10, 130), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'Check help sheet', (10, 150), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'or contact Chris', (10, 170), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'Wallace', (10, 190), angle, fonttwo, fill=(230,230,230))
        self.disp.display()

    # Display Deniedscreen
    def DrawDenied(self):
        font = ImageFont.truetype('Play With Fire.ttf',42)
        fonttwo = ImageFont.truetype('Momt___.ttf',22)
        angle = 0
        self.disp.buffer.paste((0,0,0), (0, 0, 240, 240))
        self.DrawRotatedText( \
                self.disp.buffer, 'Sorry', (10, 10), angle, font, fill=(0,0,255))
        self.DrawRotatedText(\
                self.disp.buffer, 'Badge not', (10, 90), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'recognized. To', (10, 110), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'join the coffee', (10, 130), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'club contact', (10, 150), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'Shaun Bowman', (10, 170), angle, fonttwo, fill=(230,230,230))
        self.disp.display()

    # Display Adminscreen
    def DrawAdmin(self):
        font = ImageFont.truetype('Play With Fire.ttf',42)
        fonttwo = ImageFont.truetype('MAGIMTOS.ttf',32)
        angle = 0
        self.disp.buffer.paste((50,0,0), (0, 0, 240, 240))
        self.DrawRotatedText( \
                self.disp.buffer, 'Admin', (10, 10), angle, font,
                             fill=(200,0,50))
        self.DrawRotatedText(\
                self.disp.buffer, '1 Add', (10, 70), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, '2 Remove', (10, 110), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, '3 Stats', (10, 150), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, '4 Exit', (10, 190), angle, fonttwo, fill=(230,230,230))
        self.disp.display()

    # Display Addscreen
    def DrawAdd(self):
        font = ImageFont.truetype('Play With Fire.ttf',42)
        fonttwo = ImageFont.truetype('MAGIMTOS.ttf',32)
        angle = 0
        self.disp.buffer.paste((50,0,0), (0, 0, 240, 240))
        self.DrawRotatedText( \
                self.disp.buffer, 'Admin', (10, 10), angle, font,
                             fill=(200,0,50))
        self.DrawRotatedText(\
                self.disp.buffer, 'scan', (10, 70), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'first', (10, 110), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'last', (10, 150), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, '4 Exit', (10, 190), angle, fonttwo, fill=(230,230,230))
        self.disp.display()

    # Display Removescreen
    def DrawRemove(self):
        font = ImageFont.truetype('Play With Fire.ttf',42)
        fonttwo = ImageFont.truetype('MAGIMTOS.ttf',32)
        angle = 0
        self.disp.buffer.paste((50,0,0), (0, 0, 240, 240))
        self.DrawRotatedText( \
                self.disp.buffer, 'Admin', (10, 10), angle, font,
                             fill=(200,0,50))
        self.DrawRotatedText(\
                self.disp.buffer, 'first', (10, 70), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, 'last', (10, 110), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, '3 Remove', (10, 150), angle, fonttwo, fill=(230,230,230))
        self.DrawRotatedText(\
                self.disp.buffer, '4 Exit', (10, 190), angle, fonttwo, fill=(230,230,230))
        self.disp.display()

    # Draw Recieved
    def DrawRecieved(self, x, y):
        font = ImageFont.truetype('arrow_7.ttf',42)
        angle = 0
        char = '&'
        self.DrawRotatedText( \
                self.disp.buffer, char, (x, y), angle, font,
                             fill=(200,0,50))
        self.disp.display()

    # Standbye Pulse
    def LedStandby(self):
        T_PULSE = 2
    	self.led.pulse(T_PULSE, T_PULSE, self.C_TEAL, self.C_GREEN)

    # Brew Pulse
    def LedBrew(self):
        T_PULSE = 0.5
        COLOR_ON = (1,0,1)
        COLOR_OFF = (1,1,1)
    	self.led.pulse(T_PULSE, T_PULSE, COLOR_ON, COLOR_OFF)

    # Denied Pulse
    def LedDenied(self):
        T_PULSE = 0.5
        COLOR_ON = (0,1,1)
        COLOR_OFF = (1,1,1)
    	self.led.pulse(T_PULSE, T_PULSE, COLOR_ON, COLOR_OFF)

    # Admin Pulse
    def LedAdmin(self):
        T_PULSE = 0.1
        COLOR_ON = (1,1,0.5)
        COLOR_OFF = (0.5,1,0.5)
    	self.led.pulse(T_PULSE, T_PULSE, COLOR_ON, COLOR_OFF)
