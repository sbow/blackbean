# bbdb.py
# project blackbean database class
# Shaun Bowman
# v0.1

import sqlite3
from sqlite3 import Error

class bbdb():
    cursor   = None
    conn     = None
    dbpath   = None
    dbname   = None
    fullpath = None

    def __init__(self, dbpath, dbname):
        self.create_connection(dbpath, dbname)
        self.dbpath = dbpath
        self.dbname = dbname
        self.fullpath = dbpath + dbname

    def disp_schema(self, table):
        """ Display table schema to screen
        """
        try:
            self.conn = sqlite3.connect(self.fullpath)
            self.cursor = self.conn.cursor()
            out = self.cursor.execute("PRAGMA table_info('"+table+"');").fetchall()
            for col in out:
                print(col)
        except Error as e:
            print(e)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def disp_persons(self):
        """ Display entrys to Person table
        """
        try:
            self.conn = sqlite3.connect(self.fullpath)
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM Person")
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(e)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def command(self, command):       
        """ Exect SQL command
        """
        try:
            self.conn = sqlite3.connect(self.fullpath)
            self.cursor = self.conn.cursor()
            self.cursor.execute(command)
        except Error as e:
            print(e)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
                
    def commandcommit(self, command):       
        """ Exect SQL command inserting records, executes commit
        """
        try:
            self.conn = sqlite3.connect(self.fullpath)
            self.cursor = self.conn.cursor()
            with self.conn:
                self.cursor.execute(command)
        except Error as e:
            print(e)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def commandfetchall(self, command):       
        """ Exect SQL command, return result
        """
        fetchall = None
        try:
            self.conn = sqlite3.connect(self.fullpath)
            self.cursor = self.conn.cursor()
            self.cursor.execute(command)
            fetchall = self.cursor.fetchall()
            return fetchall
        except Error as e:
            print(e)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def create_connection(self, dbpath, dbname):
        """ create a database connection to a database that resides
            on the disk
        """
        self.fullpath = dbpath + dbname 
        try:
            self.conn = sqlite3.connect(self.fullpath)
            self.cursor = self.conn.cursor()
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
       
