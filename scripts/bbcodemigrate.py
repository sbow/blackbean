# Migrate card code to code_enc
import bbsql
import bbenc

DBPATH = r''
DBNAME = r'blackbean.db'
myDb = bbsql.bbdb(DBPATH, DBNAME)
myEnc = bbenc.bbenc()
myEnc.load_public()

cards = myDb.commandfetchall("SELECT code FROM Card")
for card in cards:
    print(str(card[0]))
    encrypted = str(myEnc.encrypt(str(card[0])))
    #enc_json = myEnc.serialize(encrypted)
    print(encrypted)
    sql_update = "UPDATE Card SET code_enc = '"+encrypted+"' WHERE code ='" \
            + str(card[0]) + "';"
    print(sql_update)
    # myDb.commandcommit(sql_update) # commented out to avoid overrighting data
    sql_update = "UPDATE Card SET code = 'Secret' WHERE code ='" \
            + str(card[0]) + "';"
    # myDb.commandcommit(sql_update) # commented out to avoid overrighting data

scans = myDb.commandfetchall("SELECT code FROM Scan")
for scan in scans:
    encrypted = str(myEnc.encrypt(str(scan[0])))
    sql_update = "UPDATE Scan SET code_enc = '"+encrypted+"' WHERE code ='" \
            + str(scan[0]) + "';"
    print(sql_update)
    #myDb.commandcommit(sql_update)
    sql_update = "UPDATE Scan SET code = 'Secret'  WHERE code ='" \
            + str(scan[0]) + "';"
    print(sql_update)
    myDb.commandcommit(sql_update)
