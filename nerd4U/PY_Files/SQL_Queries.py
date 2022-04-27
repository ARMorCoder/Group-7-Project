import mysql.connector
from PY_Files import CONSTANTS
DB = mysql.connector.connect(host=CONSTANTS.HOST, user=CONSTANTS.USER,
                             password=CONSTANTS.PASSWORD, database=CONSTANTS.DATABASE)

U_TABLE = CONSTANTS.USER_TABLE
P_TABLE = CONSTANTS.PROD_TABLE
K_TABLE = CONSTANTS.KEYS_TABLE
T_TABLE = CONSTANTS.TRANS_TABLE


# sql.format(USER_TABLE,UID,USERNAME,EMAIL,PASSWORD,FIRST,LAST,STREET,STATE,SCORE,PHONE,PRIMARY)
def Push_To_User_Table(Username, Email, Password, First, Last, Street, State, phone):
    My_Cursor = DB.cursor()
    sql = "insert into {} (Username,Email,pass,First_Name,Last_Name,Address,State,Phone) values  ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    sql = sql.format(U_TABLE, Username, Email,
                     Password, First, Last, Street, State, phone)
    My_Cursor.execute(sql)
    DB.commit()

def Push_To_Trans_Table(UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,S_Address,B_Address):
    My_Cursor = DB.cursor()
    sql = "insert into {} (UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,Ship_Address,Billing_Address) values  ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    sql = sql.format(T_TABLE, UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,S_Address,B_Address)
    print(sql)
    My_Cursor.execute(sql)
    DB.commit()
def Get_Email(Email):
    return Select_Any(U_TABLE, "Email", ["Email"], [Email])


def Get_Username(Username):
    return Select_Any(U_TABLE, "Username", ["Username"], [Username])


def Get_Password(Pass):
    return Select_Any(U_TABLE, "Pass", ["Pass"], [Pass])

def Get_Password(Session_ID):
    return Select_Any(K_TABLE, "Session_ID", ["Session_ID"], [Session_ID])



def Get_Login(UserInfo):
    return Select_Any(U_TABLE, "UID", ["(Username)","(Pass)"], UserInfo)

def Get_Cart(UID):
    return Select_Any(U_TABLE, "Cart", ["UID"], [UID])


# Get_Any searches U
#
#
def Select_Any(Table, Select_List, Attribute_List, Value_List):
    My_Cursor = DB.cursor()
    sql = "Select ({}) From {} Where {}"
    Where = Format_Zip_List(Attribute_List, Value_List,"And")
    sql = sql.format(Select_List, Table, Where)
    print (sql)
    My_Cursor.execute(sql)
    returner = My_Cursor.fetchone()
    # My_Cursor.close()
    return Clean_Result(returner)


def Clean_Result(dirty):
    if(dirty == None):
        return "none"
    return dirty[0]

def Get_User_Checkout(UID):
    returner = Select_Any_Dirty(
        U_TABLE, "Address,First_Name,Last_Name", ["UID"], [UID])
    if returner != None:
        return returner
    return ("", "", "", "")

def Select_Any_Dirty(Table, Select_List, Attribute_List, Value_List):
    My_Cursor = DB.cursor()
    sql = "Select {} From {} Where {}"
    Where = Format_Zip_List(Attribute_List, Value_List, "And")
    sql = sql.format(Select_List, Table, Where)
    My_Cursor.execute(sql)
    returner = My_Cursor.fetchone()
    # My_Cursor.close()
    return returner

def Format_Zip_List(Attribute_List, Value_List,Delimiter):
    sql = '{} = "{}"'
    returner = ""
    True_Delimiter = " {} ".format(Delimiter)

    for x, y in zip(Attribute_List, Value_List):
        returner += sql.format(x, y)
        returner += True_Delimiter

    returner = returner[:-len(True_Delimiter)]
    return (returner)

def Format_Single_List(List,Delimiter):
    sql = "{}"
    Returner = ""
    True_Delimiter = " {} ".format(Delimiter)

    for x in List:
        Returner += sql.format(x)
        Returner += True_Delimiter

    Returner = Returner[:-len(True_Delimiter)]
    return (Returner)

def Format_Half_Zip_List(Value,List,Delimiter):
    sql = "{} = '{}'"
    Returner = ""
    True_Delimiter = " {} ".format(Delimiter)

    for x in List:
        Returner += sql.format(Value,x)
        Returner += True_Delimiter

    Returner = Returner[:-len(True_Delimiter)]
    return (Returner)


def Update_Field(Table,Attribute_List, Value_List, ID_Type,ID):
    My_Cursor = DB.cursor()
    update = "update {}".format(Table)
    set = "set " + Format_Zip_List([Attribute_List], [Value_List],",")
    where = 'Where {} = {}'.format(ID_Type,ID)
    sql  = "{} {} {}".format(update,set,where)
    
    My_Cursor.execute(sql)
    DB.commit()

def Fill_Cart(Cart_List):
    My_Cursor = DB.cursor()
    sql = "Select {} From {} Where {}"
    Sel_Value = "Name,Price,picture_id"
    Where = Format_Half_Zip_List("PID",Cart_List," OR ")
    sql = sql.format(Sel_Value, P_TABLE, Where)
    
    My_Cursor.execute(sql)
    return My_Cursor.fetchall()
    
def UpdateUser(uname,uid):
    My_Cursor = DB.cursor()
    My_Cursor.execute(("UPDATE user_information SET username = '{}' where UID = '{}'".format(uname,uid)))
    DB.commit()
    # My_Cursor.rowcount

def UpdatePassword(pword,uid):
    My_Cursor = DB.cursor()
    print(pword)
    My_Cursor.execute(("UPDATE user_information SET Pass = '{}' where UID = '{}'".format(pword,uid)))
    DB.commit()

def Get_Password_With_UID(uid):
    My_Cursor = DB.cursor()
    My_Cursor.execute("SELECT * from user_information where UID = '{}'".format(uid))
    result = My_Cursor.fetchone()
    return result[3]

def UpdateName(firstname,lastname,uid):
    My_Cursor = DB.cursor()
    My_Cursor.execute(("UPDATE user_information SET First_Name = '{}', Last_Name = '{}' where UID = '{}'".format(firstname,lastname,uid)))
    DB.commit()
def updatePhone(phone,uid):
    My_Cursor = DB.cursor()
    My_Cursor.execute(("UPDATE user_information SET Phone = {} where UID = '{}'".format(phone,uid)))
    DB.commit()
def UpdateEmail(email,uid):
    My_Cursor = DB.cursor()
    My_Cursor.execute(("UPDATE user_information SET Email = '{}' where UID = '{}'".format(email,uid)))
    DB.commit()
def UpdateAddress(address,state,uid):
    My_Cursor = DB.cursor()
    My_Cursor.execute(("UPDATE user_information SET Address = '{}', State = '{}' where UID = '{}'".format(address,state,uid)))
    DB.commit()
def UserIdToUsername(uid):
    My_Cursor = DB.cursor()
    My_Cursor.execute(("SELECT * FROM user_information where UID = {} ".format(uid)))
    user = My_Cursor.fetchone()
    return (user)

def Fill_Deleter(Deleter_List):
    My_Cursor = DB.cursor()
    sql = "Select {} From {} Where {}"
    Sel_Value = "PID"
    Where = Format_Half_Zip_List("name", Deleter_List, " OR ")
    sql = sql.format(Sel_Value, P_TABLE, Where)
    My_Cursor.execute(sql)
    return My_Cursor.fetchall()