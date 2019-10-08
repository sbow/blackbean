#  bbscan.py
#  2019/10/07
#  Shaun Bowman
#  
#  Scanner class for PN532 RFID Scanner
#  


import binascii
import sys

import Adafruit_PN532 as PN532


class bbscan:

    # Setup how the PN532 is connected to the Raspbery Pi/BeagleBone Black.
    # It is recommended to use a software SPI connection with 4 digital GPIO pins.
    
    # Configuration for a Raspberry Pi:
    CS   = 18
    MOSI = 20
    MISO = 19
    SCLK = 21
    
    pn532 = None
    resp  = None
    lastscan  = None
    lastuid   = None

    def __init__(self):
        # Create an instance of the PN532 class.
        self.pn532 = PN532.PN532(cs=self.CS, sclk=self.SCLK, mosi=self.MOSI,
                                 miso=self.MISO)

        # Call begin to initialize communication with the PN532.  Must be done before
        # any other calls to the PN532!
        self.pn532.begin()

        # Get the firmware version from the chip and print(it out.)
        ic, ver, rev, support = self.pn532.get_firmware_version()
        self.resp = 'Found PN532 with firmware version: {0}.{1}'.format(ver, rev)

        # Configure PN532 to communicate with MiFare cards.
        self.pn532.SAM_configuration()

    def parse(self):
        # parse current lastuid
        # Cx4Cx18Cx116Cx130Cx252Cx44Cx128
        # 4 = bb.bbsc.lastuid[0]
        # 18 = bb.bbsc.lastuid[1]
        # ...
        # 128 = bb.bbsc.lastuid[6]
        if self.lastuid is None:
            return
        else:
            parse = ''
            for i in range(len(self.lastuid)):
                parse = parse+'Cx'+str(self.lastuid[i])
            return parse

    def spin(self):
        
        while True:
            # Check if a card is available to read.
            uid = self.pn532.read_passive_target()
            # Try again if no card is available.
            if uid is None:
                continue
            self.lastuid = uid
            scan = []
            self.lastscan = []
            isData = True
            block = 1
            while isData:
                data = self.pn532.mifare_classic_read_block(block)
                if data is None:
                    isData = False
                else:
                    self.lastscan.append(data)
                    block = block + 1 
            break
