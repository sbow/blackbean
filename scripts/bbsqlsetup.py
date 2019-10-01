# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 13:49:52 2019
Sets up the initial sqlite database for blackbean coffee maker

@author: pz6hh8
"""
 
import datetime
import bbsql
from datetime import timedelta

DBPATH = r''
DBNAME = r'bbsqlite.db'

#DBPATH = r'C:\Development\sqlite3\sqlitedb'
#DBNAME = r'pythonsqlite.db'
 
myDb = bbsql.bbdb(DBPATH, DBNAME)
output = myDb.command('SELECT name from sqlite_master where type= "table"')
print(output)
sql_create_persontable =    """CREATE TABLE IF NOT EXISTS Person (
                                person_id integer PRIMARY KEY,
                                name text NOT NULL,
                                add_date text
                                );
                            """
myDb.command(sql_create_persontable)
print("\nPerson Schema:")
myDb.disp_schema('Person')

sql_create_cardtable =      """CREATE TABLE IF NOT EXISTS Card (
                                card_id integer PRIMARY KEY,
                                code text NOT NULL,
                                add_date text,
                                active text DEFAULT 'Y',
                                person_id integer NOT NULL,
                                FOREIGN KEY (person_id)
                                    REFERENCES Person (person_id)
                                );
                            """
myDb.command(sql_create_cardtable)
print("\nCard Schema:")
myDb.disp_schema('Card')

fp = open('./olddata/MEMBERS_with_names.txt', 'r')
data = fp.readlines()
print("\n")
fp.close()
# name: data[0].split(',')[1].strip()
# _ID_: data[0].split(',')[0].strip()
# strip takes out leading/trailing whitespace
parsed = [[i.strip() for i in j.split(',')] for j in data]

i = 0
names = []
for entry in parsed:
    if len(entry) == 1:
        i = i + 1
        name = "Mystery Person " + str(i)
    else:
        name = entry[1]
    names.append(name)        
    print(name)

# Matches will contain the index of first occurance of a name.
# Some people have gotten replacement ID cards and appear more
# than once.
matches = [0]
for i in range(1,len(names),1):
    found = False
    for j in range(i-1):
        if not found:
            if names[i] == names[j]:
                matches.append(j)
                found = True
    if not found:
        matches.append(i)
    #print(parsed[i][0] + " " + str(matches[i]) + " " + names[ matches[i] ])

# Code to populate people - only populate if matches[i] == i (ie: first time)
club_start_date = datetime.date(2018, 3, 19)
for i in range(len(matches)):
    if matches[i] == i:
        # unique name - add
        name = names[i]
        date = club_start_date.isoformat()
        sql_insert_persons =    """ INSERT INTO Person (name, add_date)
                                    VALUES ('""" + name + "', '" + date + "');"
        print(sql_insert_persons)
        #myDb.commandcommit(sql_insert_persons) # commented out to not duplicate

# Code to populate cards - for some people, there are is more than one card
person_ids = []
club_start_date = datetime.date(2018, 3, 19)
date = club_start_date.isoformat()
for i in range(len(matches)):
    idMatch = myDb.commandfetchall("SELECT person_id FROM Person WHERE name in('" \
                                + names[matches[i]] + "')")
    person_ids.append(idMatch[0][0])
    print(idMatch[0])
    sql_insert_card =   " INSERT INTO Card(code, add_date, person_id)" \
                        +" VALUES ('" + parsed[i][0]+"', '" + date + "', '" \
                        + str(person_ids[i]) + "');"
    print(sql_insert_card)
    #myDb.commandcommit(sql_insert_card) # commented out to not duplicate

# Code to create a table to store scan events 
sql_create_scantable =      """CREATE TABLE IF NOT EXISTS Scan (
                                scan_id integer PRIMARY KEY,
                                code text NOT NULL,
                                scan_date text,
                                date_real text
                                );
                            """
myDb.command(sql_create_scantable)
print("\nScan Schema:")
myDb.disp_schema('Scan')

# Code to populate scans from old data - fake times, but maintaining sequence
fp = open('./olddata/BREWLOG.txt', 'r') # format: "12, C02x390x493x090"
data = fp.readlines()
print("\n")
fp.close()
parsed = [[i.strip() for i in j.split(',')] for j in data]
# ^ parsed[11] = ['12', 'C02x390x493x090']
i = 0
for scan in parsed:
    date = timedelta(hours=i) + club_start_date # assume 1 scan per hour
    i = i + 1
    sql_insert_scan =   " INSERT INTO Scan(code, scan_date, date_real)" \
                        +" VALUES ('"+scan[1]+"', '"+date.isoformat()+"', 'N');"
    #print(sql_insert_scan)
    #myDb.commandcommit(sql_insert_scan) # commented out to not duplicate

# Code to create drink events
sql_create_drinktable =      """CREATE TABLE IF NOT EXISTS Drink (
                                drink_id integer PRIMARY KEY,
                                card_id integer NOT NULL,
                                scan_date text NOT NULL,
                                date_real text NOT NULL,
                                person_id integer NOT NULL,
                                FOREIGN KEY (card_id)
                                    REFERENCES Card (card_id),
                                FOREIGN KEY (scan_date)
                                    REFERENCES Scan (scan_date),
                                FOREIGN KEY (date_real)
                                    REFERENCES Scan (date_real),
                                FOREIGN KEY (person_id)
                                    REFERENCES Person (person_id)
                                );
                            """
myDb.command(sql_create_drinktable)
print("\nDrink Schema:")
myDb.disp_schema('Drink')

# Code to populate drink events from scan events
scans = myDb.commandfetchall("SELECT * FROM Scan")
# ^scans[-1] = ['scan_id', 'code', 'scan_date', 'date_real']
for scan in scans:
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
                            # yDb.commandcommit(sql_write_drink) # commentedout 
            else:
                print('Card not active')

