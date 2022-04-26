from PY_Files import SQL_Queries, CONSTANTS


def Login_User(Username, Password):
    return SQL_Queries.Get_Login([Username,Password])
    
    

# def Create_Session_Id(User_ID):
#     Session_ID = str(User_ID)
#     while(len(User_ID)):
#         Session_ID = "0"+ Session_ID
