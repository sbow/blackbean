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
#    computer is also connected to a RFID reader. 
#    If a member scan's their card, and the card
#    number matches one wherin they have access to
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
import blackbean
from time import sleep
import time
import threading
DBPATH = r''
DBNAME = r'bbsqlite.db'


def Scan(bb, scan, date):
    sql_insert_scan =   " INSERT INTO Scan(code_enc, scan_date, date_real, code, code_encrypt)" \
                        +" VALUES ('"+scan+"', '"+date+"', 'Y', 'Secret', 'Secret');"
    print(sql_insert_scan)
    bb.bbdb.commandcommit(sql_insert_scan) # commented out to not duplicate

def Drink(bb, scan):
    scan = scan[0]
    scan_id = scan[0]
    code = scan[6]   # note, code is encrypted
    scan_date = scan[2]
    date_real = scan[3]
    sql_find_code = "SELECT card_id FROM Card WHERE code_enc in('"+code+"');"
    print("Scan ID:" + str(scan_id) + " Code_enc=" + code + " scan_date=" + scan_date)
    found_card = bb.bbdb.commandfetchall(sql_find_code)
    if found_card != []:
        # found card
        card_id = found_card[0][0]
        sql_det_acces = "SELECT active FROM Card WHERE code_enc in('"+code+"');"
        is_active = bb.bbdb.commandfetchall(sql_det_acces)
        if is_active == []:
            print('Card not found')
            return(0)
        else:
            if is_active[0][0] == "Y":
                # card is authorized for drink
                print('Yes for drink')
                sql_det_scan_date = "SELECT scan_date FROM Scan WHERE scan_id"\
                                    " in('"+str(scan_id)+"');"
                found_scan_date = bb.bbdb.commandfetchall(sql_det_scan_date)
                if found_scan_date == []:
                    print('Scan date not found')
                    return(0)
                else:
                    print('Scan date: '+found_scan_date[0][0])
                    scan_date = found_scan_date[0][0]
                    sql_det_scan_real = "SELECT date_real FROM Scan WHERE \
                            scan_id in('"+str(scan_id)+"');"
                    found_date_real = bb.bbdb.commandfetchall(sql_det_scan_real)
                    if found_date_real ==[]:
                        print('Could not determine if date_real was real')
                        return(0)
                    else:
                        print('Scan date real: '+found_date_real[0][0])
                        sql_get_personid = "SELECT person_id FROM Card WHERE \
                                code_enc in ('"+code+"');"
                        found_person_id = \
                        bb.bbdb.commandfetchall(sql_get_personid)
                        if found_person_id == []:
                            print('Cound not determine person_id')
                            return(0)
                        else:
                            print('Person_id: ' + str(found_person_id[0][0]))
                            sql_write_drink = "INSERT into Drink(card_id, " \
                                + "scan_date, date_real, person_id) VALUES('" \
                                + str(card_id) + "','" + scan_date + "','" \
                                + found_date_real[0][0] + "','" \
                                + str(found_person_id[0][0]) + "');" 
                            print(sql_write_drink)
                            bb.bbdb.commandcommit(sql_write_drink) # commentedout 
                            return(1)
            else:
                print('Card not active')
                return(0)

def DoStandby():
    bb.DrawHome()
    bb.LedStandby()
    t = threading.Timer(3600.0, DoScreensaver, [bb])
    t.start() # after 1hr turn off display, leave LED
    bb.bbsc.spin() # wait for scan
    t.cancel()
    code = bb.bbsc.parse() # get scan result
    encrypted = str(bb.bbenc.encrypt(code))
    #enc_json = bb.bbenc.serialize(encrypted)
    DoScan(bb, encrypted)

def DoAdmin():
    bb.DrawAdmin()
    bb.LedAdmin()
    num = raw_input()
    if num == '1':
        print('1')
        DoAdd()
    elif num == '2':
        print('2')
        DoRemove()
    elif num == '3':
        print('3')
    else:
        print('exit')
        DoStandby()

def DoAdd():
    bb.DrawAdd()
    entry = raw_input()
    if entry == '4':
        DoStandby()
    else:
        first = entry
        print(entry)
        bb.DrawRecieved(200, 120)
        entry = raw_input()
        if entry == '4':
            DoStandby()
        else:
            last = entry
            print(entry)
            bb.DrawRecieved(200, 160)
            DoStandby()

def DoRemove():
    bb.DrawRemove()
    entry = raw_input()
    if entry == '4':
        DoStandby()
    else:
        first = entry
        print(entry)
        bb.DrawRecieved(200, 80)
        entry = raw_input()
        if entry == '4' or entry =='3':
            DoStandby()
        else:
            last = entry
            print(entry)
            bb.DrawRecieved(200, 120)
            entry = raw_input()
            if entry == '3':
                print('remove')
                bb.DrawRecieved(200, 160)
                DoStandby()
            else:
                DoStandby()
def DoDenied():
    bb.DrawDenied()
    bb.LedDenied()
    sleep(10)
    DoStandby()

def DoBrew():
    bb.DrawBrew()
    bb.RelayOn()
    sleep(4)
    bb.RelayOff()
    bb.LedBrew()
    sleep(20)
    DoStandby()

def DoScan(bb, code):
    #note code is encrypted
    time = datetime.datetime.now().isoformat()
    Scan(bb, code, time)
    lastscan = bb.bbdb.commandfetchall('SELECT * FROM Scan ORDER BY \
                                       scan_id DESC LIMIT 1')
    DoDrink(bb, lastscan)

def DoDrink(bb, scanrecord):
    print('DoDrink')
    passfail = Drink(bb, scanrecord)
    if passfail == 1:
        DoBrew()
    else:
        DoDenied()

def DoScreensaver(bb):
    # called by timer
    bb.disp.clear()

# MAIN:
bb = blackbean.bbrun() # start blackbean program
bb.DrawHome() # display homescreen
bb.LedStandby()  # pulse LED
bb.DrawBrew()
bb.LedBrew()
bb.DrawDenied()
bb.LedDenied()
bb.DrawAdmin()
bb.LedAdmin()
DoStandby()
