import mysql.connector
from PY_Files import CONSTANTS
DB = mysql.connector.connect(host=CONSTANTS.HOST, user=CONSTANTS.USER,
                             password=CONSTANTS.PASSWORD, database=CONSTANTS.DATABASE)

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
