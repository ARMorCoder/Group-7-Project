import mysql.connector
from PY_Files import CONSTANTS
DB = mysql.connector.connect(host=CONSTANTS.HOST, user=CONSTANTS.USER,
                             password=CONSTANTS.PASSWORD, database=CONSTANTS.DATABASE)

from PY_Files import SQL_Queries
import datetime

# 3417822654878618
def Create_Transaction_Tuple(UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,S_Address,B_Address):
    print((UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,S_Address,B_Address))
    SQL_Queries.Push_To_Trans_Table(UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,S_Address,B_Address)

def Make_Address_String(Street, State, City, Zip, Suite):
    return "{} #{} {} {} {}".format(Street,Suite,Zip,State,City)

def Make_Cart_Names(Tuple_List):
    returner = ""
    for each in Tuple_List:
        returner = returner + each[0] + ","
    return "[{}]".format(returner[:-1])

def Get_Date():
    Dater = datetime.datetime.now()
    return "{}/{}/{}".format(Dater.month,Dater.day,Dater.year)

def Redact_CC(CC):
    Last_4 = str(CC)[-4:]
    Redaction = ""
    for i in range(0,len(str(CC)[:-4])):
        Redaction += "*"
    return Redaction + Last_4

def Complete_Transaction():
    pass

def Pull_Transactions_From_UID(uid):
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM trans_information where UID = '" + uid + "'")
    array = cursor.fetchall()
    return (array)
    
def Get_Products_From_Cart(pid):
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM product_information where PID = '" + pid + "'")
    array = cursor.fetchone()
    return (array)