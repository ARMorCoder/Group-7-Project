import mysql.connector
from PY_Files import CONSTANTS
DB = mysql.connector.connect(user="jtmoney", password="HelpHimRnPlz1327!", host="nerd4u-ecommerce-database.mysql.database.azure.com", port=3306, database="nerd4u")

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
