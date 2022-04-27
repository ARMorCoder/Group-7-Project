from distutils.command.install_lib import PYTHON_SOURCE_EXTENSION
import mysql.connector

import CONSTANTS
DB = mysql.connector.connect(host=CONSTANTS.HOST, user=CONSTANTS.USER,
                             password=CONSTANTS.PASSWORD, database=CONSTANTS.DATABASE)


def Drop_table():

    My_Cursor = DB.cursor()
    sql = "DROP TABLE if exists {};"
    sql = sql.format(CONSTANTS.USER_TABLE)
    My_Cursor.execute(sql)


UID = "UID        INT             NOT NULL AUTO_INCREMENT"
USERNAME = "Username   VARCHAR(255)    NOT NULL"
EMAIL = "Email      VARCHAR(255)    NOT NULL"
PASSWORD = "Pass       VARCHAR(30)     NOT NULL"
FIRST = "First_Name VARCHAR(255)    NOT NULL"
LAST = "Last_Name  VARCHAR(255)    NOT NULL"
STREET = "Address    VARCHAR(255)    NOT NULL"
STATE = "State      CHAR(2)         NOT NULL"
PHONE = "Phone      CHAR(10)        NOT NULL"
SCORE = "Score      CHAR(2)"
PRIMARY = "PRIMARY KEY (UID)"
START_UID = "ALTER TABLE {} AUTO_INCREMENT=100".format(CONSTANTS.USER_TABLE)


def Make_Table():
    My_Cursor = DB.cursor()
    # sql = '''Create Table {} ({}, {}, {},{}, {},{}, {},{},{},{},{});'''

    sql = '''CREATE TABLE {} (
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {},
                          {});'''

    sql = sql.format(CONSTANTS.USER_TABLE, UID, USERNAME, EMAIL,
                     PASSWORD, FIRST, LAST, STREET, STATE, PHONE, SCORE, PRIMARY)
    print(sql)
    My_Cursor.execute(sql)
    sql = START_UID
    My_Cursor.execute(sql)


Drop_table()
Make_Table()
