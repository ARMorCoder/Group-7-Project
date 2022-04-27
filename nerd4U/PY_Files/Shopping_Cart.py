# session id -> UID
# UID -> Shopping Cart lsit(as a string)
# convert string to list of Pid
# get Select pids
# paste pids into cart
from PY_Files import SQL_Queries,CONSTANTS

# adds PID to a shopping cart field in DB
def Add_To_Cart(UID,PID):
    Cart = Pull_Cart(UID)
    Cart = Add_Item(Cart,PID)
    Push_Cart(Cart,UID)

# 
def Push_Cart(Temp_Cart,UID):
    SQL_Queries.Update_Field(CONSTANTS.USER_TABLE,"Cart",Temp_Cart,"UID",UID)

# Makes a list from a cart's uid
def Pull_Cart(UID):
    Cart_List = SQL_Queries.Get_Cart(UID)
    Cart_List = Cart_List[1:-1]
    Cart_List = Cart_List.split(',')
    Cart_List = Str_To_Lint(Cart_List)
    return Cart_List

# adds a pid to a list cart
def Add_Item(Cart_List, New_PID):
    PID_Set = set(Cart_List)
    if New_PID not in PID_Set:
        PID_Set.add(New_PID)
        Cart_List.insert(0,New_PID)
    Cart_List.sort()
    return Cart_List


def Str_To_Lint(String_List):
    for i in range(0, len(String_List)):
        String_List[i] = int(String_List[i])
    return String_List

def Delete_From_Cart(UID,PID):
    Cart = Pull_Cart(UID)
    Cart.remove(PID)
    Push_Cart(Cart,UID)

def Get_Shopping_Products(cart_list):
     return SQL_Queries.Fill_Cart(cart_list)

