# blackbean.py
#
# An office coffee machine controller
# 
# v0.1
# 2019/09/12
#- initial framework of controller

PIN_RELAY = 26
PIN_RED   = 5
PIN_GREEN = 6
PIN_BLUE  = 4

C_GREEN = (1,0.5,1)
C_TEAL  = (1,0.8,0.5)

T_PULSE = 0.5

from gpiozero import RGBLED, LED
from time import sleep

led = RGBLED(PIN_RED, PIN_GREEN, PIN_BLUE)
relay = LED(PIN_RELAY)

led.pulse(T_PULSE, T_PULSE, C_TEAL, C_GREEN)

sleep(10)
