# BlackBean
![Blackbean Logo](https://raw.githubusercontent.com/sbow/blackbean/master/blackbean.png)

Project Blackbean - a controller for a office coffee machine.


## Hardware
- Raspberry PI Zero W
- Sandisk 16 gb micro SD card
- Raspberry pi USB power supply
- Generic 5v low closing current relay (Solidstate is a poor choice - inconsistant switching, ie Omron G3NA-210B)
- RGB LED (CA, PN: Q16F5CZZRGB24ECA)
- TFT Display (Adafruit ST7789 1.3" 240x240)
- (Card reader)
- Logitech K400+ keyboard and trackpad


## Quick Start
Clone the repo:
```
cd 
git clone https://github.com/sbow/blackbean
cd blackbean
```

Create a blackbean object & demo the display:
```
cd ./scripts
python
import blackbean
bb = blackbean.bbrun()
bb.TftDemo()
```

## Wiring: 
| Componant     | Label | Componant  | Label |
| ------------- |:-----:| ---------- |:-----:|
| RGB LED       | black | RPi        | 3V3   |
| RGB LED       | red   | RPi        | 5     |
| RGB LED       | green | RPi        | 6     |
| RGB LED       | blue  | Rpi        | 4     |
| Relay         | -     | Rpi        | Gnd   |
| Relay         | +     | Rpi        | 4     |
| Relay         | s     | Rpi        | 26    |
| Relay         | NC    | Coffee     | brew  |
| Relay         | COM   | Coffee     | brew  |
| TFT Display   | Lite  | No Connect |       |
| TFT Display   | CCS   | No Connect |       |
| TFT Display   | D/C   | Rpi        | 24    |
| TFT Display   | RST   | Rpi        | 23    |
| TFT Display   | TCS   | Rpi        | CE0   |
| TFT Display   | SI    | Rpi        | MOSI  |
| TFT Display   | SO    | No Connect |       |
| TFT Display   | SCK   | Rpi        | SCLK  |
| TFT Display   | Gnd   | Rpi        | Gnd   |
| TFT Display   | 3v3   | Rpi        | 3V3   |
| TFT Display   | Vin   | No Connect |       |
| Ada PN532 1.3 | Gnd   | Rpi        | Gnd   |
| Ada PN532 1.3 | Vin   | No Connect |       |
| Ada PN532 1.3 | 5v    | Rpi        | 5v    |
| Ada PN532 1.3 | 3v    | Rpi        | 3.3v  |
| Ada PN532 1.3 | MOSI  | Rpi        | 20    |
| Ada PN532 1.3 | SS    | Rpi        | 18    |
| Ada PN532 1.3 | MISO  | Rpi        | 19    |
| Ada PN532 1.3 | SCK   | Rpi        | 21    |
| Ada PN532 1.3 | RST   | No Connect |       |
| Ada PN532 1.3 | IRQ   | No Connect |       |

