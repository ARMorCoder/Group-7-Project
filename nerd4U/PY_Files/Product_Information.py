import mysql.connector

db = mysql.connector.connect(host="user-information.cfe8lazrwbtc.us-east-1.rds.amazonaws.com",
                             user="admin", password="password", database="user")

TABLE_NAME = "product_information"

#########################################
## Queries Database for products that  ##
## have specified category.            ##
#########################################


def Get_Product_By_Catagory(category):
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM product_information where catagory = '" + category + "'")
    array = cursor.fetchall()
    return (array)


def Get_Product_By_Category_If_Valid(array, category):
    cursor = db.cursor()
    test = "%" + str(array[0][10]) + "%"
    # make a new string with spliced list
    cursor.execute("SELECT * FROM product_information where catagory like '%" +
                   category + "%' AND  tags like '" + test + "'")
    array = cursor.fetchall()
    return (array)


def Get_Product_By_Tag(tag):
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM product_information where tags like '%" + tag + "%'")
    array = cursor.fetchall()
    return (array)


def Get_Product_By_SubCategory(subcategory, title):
    cursor = db.cursor()
    test = "" + str(title) + ""
    cursor.execute("SELECT * FROM product_information where sub_category like '%" +
                   subcategory + "%' AND  name like '" + test + "'")
    array = cursor.fetchall()
    return (array)


def Insert_New_Product(list_of_tags, title, description, image, price, quantity, catagory, subcategory):

    cursor = db.cursor()

    sql = "INSERT INTO product_information (name, price, picture_id, seller_id, description, quantity, remaining_item, catagory, sub_category, tags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # CHANGE PRICE (DOLLAR) TO ACTUAL SUM OF DOLLAR + CENT
    val = (title, price, image, 1, description, quantity,
           quantity, catagory, subcategory, str(list_of_tags))
    cursor.execute(sql, val)
    db.commit()


def strArrayToArray(array):
    new_array = []
    array = array[1:-1]
    array = array.split(',')
    for i in range(0, len(array)):
        array[i] = array[i].strip()
        new_array.append(array[i].strip("'"))

    return new_array
