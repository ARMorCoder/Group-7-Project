from PY_Files import SQL_Queries, REGEX


# sql.format(USER_TABLE,UID,USERNAME,EMAIL,PASSWORD,FIRST,LAST,STREET,STATE,SCORE,PHONE,PRIMARY)
def Create_User(Username, Email, Password, First, Last, Street, State, Phone):
    Code = Verify_Duplicate(Username, Email)
    if (Code == 0):

        SQL_Queries.Push_To_User_Table(
            Username, Email, Password, First, Last, Street, State, Phone)
    return Code

# Returns a string from a Dupe code


def Login_Code_Statement(Dupe_Code):
    if (Dupe_Code == 0):
        Dupe_Statement = "Registration Sucessful"
    if (Dupe_Code == 1):
        Dupe_Statement = "That Username is already in use"
    if (Dupe_Code == 2):
        Dupe_Statement = "That Email Address is already in use"
    if (Dupe_Code == 3):
        Dupe_Statement = "That Username and Email Address is already in use"
    return Dupe_Statement


# Verify_Duplicate returns an int code of possible duplication
# 0 is no dupe
# 1 is dupe Name
# 2 is dupe Email
# 3 is dupe Both
#
def Verify_Duplicate(Username, Email):
    Temp_SQL_Results = Run_Dupe_SQL_Search(Username, Email)
    Dupe_Code = 0
    if(Username == Temp_SQL_Results[0]):
        Dupe_Code += 1

    if(Email == Temp_SQL_Results[1]):
        Dupe_Code += 2

    return Dupe_Code


def Run_Dupe_SQL_Search(Username, Email):
    a = SQL_Queries.Get_Username(Username)
    b = SQL_Queries.Get_Email(Email)
    return [a, b]
