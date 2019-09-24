from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_ST7789 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time

# Raspberry Pi configuration.
DC = 24
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Create TFT LCD display class.
disp = TFT.ST7789(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))

# Initialize display.
disp.begin()

# Clear the display to a red background.
# Can pass any tuple of red, green, blue values (from 0 to 255 each).
disp.clear((0, 0, 0))

# Alternatively can clear to a black screen by calling:
# disp.clear()

# Get a PIL Draw object to start drawing on the display buffer.
draw = disp.draw()

# Load default font.
#font = ImageFont.truetype('MAGIMTOS.ttf',32)
#font = ImageFont.truetype('Momt___.ttf',32)
#font = ImageFont.truetype('Mexicanero.ttf',32)
font = ImageFont.truetype('Play With Fire.ttf',42)
fonttwo = ImageFont.truetype('Momt___.ttf',22)

# Alternatively load a TTF font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 16)

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

draw_rotated_text(disp.buffer, 'Coffee', (180, 10), 270, font, fill=(255,255,255))
draw_rotated_text(disp.buffer, 'Club', (120, 10), 270, font, fill=(255,255,255))
draw_rotated_text(disp.buffer, 'Scan Badge', (30, 10), 270, fonttwo, fill=(255,255,255))
draw_rotated_text(disp.buffer, 'For Coffee', (10, 10), 270, fonttwo, fill=(255,255,255))

# Write buffer to display hardware, must be called to make things visible on the
# display!
disp.display()

# for i in range(3):
# 
#     draw_rotated_text(disp.buffer, 'Hello World!', (50, 10), int(i/3.0*360), font, fill=(255,255,255))
#     disp.display()
#     #time.sleep(0.1)
