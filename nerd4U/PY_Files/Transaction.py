import datetime
import SQL_Queries

def Create_Transaction_Tuple(UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,S_Address,B_Address):
    SQl_Queries.Push_To_Trans_Table(UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,S_Address,B_Address)

def Make_Address_String(Street, State, City, Zip, Suite):
    return "{} #{} {} {} {}".format(Street,Suite,Zip,State,City)

def Make_Cart_Names(Tuple_List):
    returner = ""
    for each in Tuple_List:
        returner = returner + each[0] + ","
    return "[{}]".format(returner[:-1])

def Get_Date():
    return datetime.datetime.now

def Redact_CC(CC):
    Last_4 = str(CC)[-4:]
    Redaction = ""
    for i in range(0,len(str(CC)[:-4])):
        Redaction += "*"
    return Redaction + Last_4

def Complete_Transaction():
    pass