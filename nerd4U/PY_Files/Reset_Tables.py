from distutils.command.install_lib import PYTHON_SOURCE_EXTENSION
import mysql.connector

import CONSTANTS
DB = mysql.connector.connect(host=CONSTANTS.HOST, user=CONSTANTS.USER,
                             password=CONSTANTS.PASSWORD, database=CONSTANTS.DATABASE)


def Drop_table(Table):

    My_Cursor = DB.cursor()
    sql = "DROP TABLE if exists {};"
    sql = sql.format(Table)
    My_Cursor.execute(sql)


UID = "UID        INT             NOT NULL AUTO_INCREMENT"
USERNAME = "Username   VARCHAR(256)    NOT NULL"
EMAIL = "Email      VARCHAR(256)    NOT NULL"
PASSWORD = "Pass       VARCHAR(30)     NOT NULL"
FIRST = "First_Name VARCHAR(256)    NOT NULL"
LAST = "Last_Name  VARCHAR(256)    NOT NULL"
STREET = "Address    VARCHAR(256)    NOT NULL"
STATE = "State      CHAR(2)         NOT NULL"
PHONE = "Phone      CHAR(10)        NOT NULL"
SCORE = "Score      CHAR(2)"
CART = "Cart         VARCHAR(256)"
PRIMARY = "PRIMARY KEY (UID)"

USERFIELDS = [UID, USERNAME, EMAIL, PASSWORD, FIRST,
              LAST, STREET, STATE, PHONE, SCORE, CART, PRIMARY]

Pid = "PID int not null auto_increment"
INAME = "name varchar(256)"
Price = "price varchar(20)"
Pic_Id = "picture_id varchar(256)"
SID = "seller_id int"
DEsc = "description varchar(256)"
Quantity = "quantity int"
Remaining = "remaining_item int"
catagory = "catagory varchar(256)"
sub_category = "sub_category varchar(256)"
tags = "tags varchar(256)"
PPrimary = "PRIMARY KEY (PID)"
PRODFIELDS = [Pid, INAME, Price, Pic_Id, SID, DEsc, Quantity,
              Remaining, catagory, sub_category, tags, PPrimary]

TID = "TID int not null auto_increment"
TUID = "UID int not null"
Cart_IDs = "Cart_IDs varchar(256)"
Cart_Names = "Cart_Names varchar(256)"
Taxed_Total = "Taxed_Total varchar(256)"
Date = "Date varchar(256)"
Payment_Info = "Payment_Info varchar(16)"
Ship_Address = "Ship_Address varchar(256)"
Billing_Address = "Billing_Address varchar(256)"
TPrimary = "PRIMARY KEY (TID)"
T_FIELDS = [TID, TUID, Cart_IDs, Cart_Names, Taxed_Total, Date, Payment_Info,
              Ship_Address, Billing_Address, TPrimary]


START_ID = "ALTER TABLE {} AUTO_INCREMENT=100"


def Make_User_Table():
    Make_Table(CONSTANTS.USER_TABLE, USERFIELDS)


def Make_Prod_Table():
    Make_Table(CONSTANTS.PROD_TABLE, PRODFIELDS)

def Make_T_Table():
    Make_Table(CONSTANTS.TRANS_TABLE, T_FIELDS)


def Make_Table(userTable, newfields):
    My_Cursor = DB.cursor()

    sql = 'CREATE TABLE {} ({})'
    fields = Format_Statement(newfields)
    sql = sql.format(userTable, fields)
    print(sql)
    My_Cursor.execute(sql)
    sql = START_ID.format(userTable)
    print(sql)
    My_Cursor.execute(sql)


def Format_Statement(list):
    sql = "{}"
    returner = ""

    for x in list:
        returner += sql.format(x,)
        returner += " , "

    returner = returner[:-len(" , ")]
    return (returner)
