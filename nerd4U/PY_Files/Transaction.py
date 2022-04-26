import datetime
def Create_Transaction_Tuple(TID,UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,Address):
    return (TID,UID,Cart_IDs,Cart_Names,Taxed_Total,Date,Payment_Info,Address)

def Make_Address_String(Street, State, City, Zip, Suite):
    return "{}{} {} {} {}".format(Street,Suite,Zip,State,City)

def Get_Date():
    return datetime.datetime.now

def Complete_Transaction():
    