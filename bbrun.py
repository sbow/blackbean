#    bbrun.py
#    Created on Sep 30 2019
#    v0.1
#    Author: shaun bowman
#    SRC: https://github.com/sbow/blackbean
#    Licece: MIT
#
#    This is the 'main' program for project blackbean.
#    Project blackbean is an office coffee maker that
#    has had its "brew" button short-cirtuited via a
#    relay connected to a Raspbery-Pi computer. The 
#    computer is also connected to a RFID reader. The
#    reader is able to read the company ID card 
#    employees carry with them to access the building.
#    If an employee scan's their badge, and the badge
#    ID number matches one wherin they have access to
#    the coffe maker - the raspberry pi via this
#    program causes a relay to close such that the 
#    brew button is pressed & a coffee is brewed.
#    Other fucntions include special ID's linked to
#    RFID access devices providing "administrator"
#    access. When such an ID is detected, the 
#    software prompts the user that the next ID 
#    scanned will have its access modified. After 
#    this ID is scanned - the administrator has the
#    option to add or remove access to the coffee 
#    machine.

#Coffee Maker Database Setup
import datetime
from datetime import timedelta
import bbsql
DBPATH = r''
DBNAME = r'bbsqlite.db'

#TFT Display Setup - ST7789 Adafruit 240x240 1.54" SPI
PIN_DC = 24 
PIN_RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

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

def scan(scan, date):
    sql_insert_scan =   " INSERT INTO Scan(code, scan_date, date_real)" \
                        +" VALUES ('"+scan[1]+"', '"+date.isoformat()+"', 'N');"
    print(sql_insert_scan)
    #myDb.commandcommit(sql_insert_scan) # commented out to not duplicate

def drink(myDb, scan):
    scan_id = scan[0]
    code = scan[1]
    scan_date = scan[2]
    date_real = scan[3]
    sql_find_code = "SELECT card_id FROM Card WHERE code in('"+code+"');"
    print("Scan ID:" + str(scan_id) + " Code=" + code + " scan_date=" + scan_date)
    found_card = myDb.commandfetchall(sql_find_code)
    if found_card != []:
        # found card
        card_id = found_card[0][0]
        sql_det_acces = "SELECT active FROM Card WHERE code in('"+code+"');"
        is_active = myDb.commandfetchall(sql_det_acces)
        if is_active == []:
            print('Card not found')
        else:
            if is_active[0][0] == "Y":
                # card is authorized for drink
                print('Yes for drink')
                sql_det_scan_date = "SELECT scan_date FROM Scan WHERE scan_id"\
                                    " in('"+str(scan_id)+"');"
                found_scan_date = myDb.commandfetchall(sql_det_scan_date)
                if found_scan_date == []:
                    print('Scan date not found')
                else:
                    print('Scan date: '+found_scan_date[0][0])
                    scan_date = found_scan_date[0][0]
                    sql_det_scan_real = "SELECT date_real FROM Scan WHERE \
                            scan_id in('"+str(scan_id)+"');"
                    found_date_real = myDb.commandfetchall(sql_det_scan_real)
                    if found_date_real ==[]:
                        print('Could not determine if date_real was real')
                    else:
                        print('Scan date real: '+found_date_real[0][0])
                        sql_get_personid = "SELECT person_id FROM Card WHERE \
                                code in ('"+code+"');"
                        found_person_id = \
                        myDb.commandfetchall(sql_get_personid)
                        if found_person_id == []:
                            print('Cound not determine person_id')
                        else:
                            print('Person_id: ' + str(found_person_id[0][0]))
                            sql_write_drink = "INSERT into Drink(card_id, " \
                                + "scan_date, date_real, person_id) VALUES('" \
                                + str(card_id) + "','" + scan_date + "','" \
                                + found_date_real[0][0] + "','" \
                                + str(found_person_id[0][0]) + "');" 
                            print(sql_write_drink)
                            # myDb.commandcommit(sql_write_drink) # commentedout 
            else:
                print('Card not active')

    dev main():

