import re
from re import A
import sys
import os
from ast import literal_eval

# password: passwordtodb123!

import mysql.connector
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, session, flash


from PY_Files import Create_User, Login_User, CONSTANTS, SQL_Queries, Product_Information, Shopping_Cart


app = Flask(__name__, static_folder='./static')

app.secret_key = 'super secret key'

# Connect to database

DB = mysql.connector.connect(host=CONSTANTS.HOST, user=CONSTANTS.USER,
                             password=CONSTANTS.PASSWORD, database=CONSTANTS.DATABASE)
## Home Page ##


@app.route('/', methods=['GET', 'POST'])
def homepage():

    if request.method == 'POST':

        search_for = request.form['search_bar']
        session["search_for"] = search_for
        # print(session["search_for"])

        return redirect(url_for('searchpage'))

    ################################################################################################
    # Call function to perform SQL Query on specified categories (returns array containing tuples) #
    #
    art_products = Product_Information.Get_Product_By_Catagory('Art')
    print(art_products)                                               #
    comic_products = Product_Information.Get_Product_By_Catagory(
        'Comics')                                             #
    toy_products = Product_Information.Get_Product_By_Catagory(
        'Toys & Models')                                        #

    #####################################################################################
    # Recurse through each tuple, only returning the third data column (the image id's) #
    #####################################################################################
    #
    #
    #
    art_img_ids = (tuple(map(lambda x: x[3], art_products)))
    #
    #
    comic_img_ids = (
        tuple(map(lambda x: x[3], comic_products)))                        #
    #
    #
    #
    #
    toy_img_ids = (tuple(map(lambda x: x[3], toy_products)))
    #

    return render_template('homepage.html',
                           art_img_ids=art_img_ids,
                           comic_img_ids=comic_img_ids,
                           toy_img_ids=toy_img_ids,
                           art_products=art_products,
                           comic_products=comic_products,
                           toy_products=toy_products
                           )  # Display's homepage when at root directory of website along with all products ##

## Helper Function ##


@app.route('/upload/<filename>')
def send_image(filename):

    # Display images
    print(filename)
    return send_from_directory("../Images", filename)


## User Login Page ##


@app.route('/userLogin', methods=['GET', 'POST'])
def login():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access

        username = request.form['username']
        passw = request.form['password']

        account = Login_User.Login_User(username, passw)
        if account == "none":
            flash('Incorrect User information')
        else:
            session["UID"] = account
            flash('Login Sucessful UID:{}'.format(account))
            # Redirect to home page
            return redirect(url_for('homepage'))

    # Show the login form with message (if any)

    return render_template('login.html')


@app.route('/userRegristration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        street_address = request.form['street_address']
        state = request.form['state']
        phone_number = request.form['phone_number']

        Flash_Code = Create_User.Create_User(
            username, email, password, first_name, last_name, street_address, state, phone_number)
        Flash_Statement = Create_User.Login_Code_Statement(Flash_Code)
        # print(tempflash)
        flash(Flash_Statement)
        if Flash_Code == 0:
            return redirect(url_for('homepage'))

    return render_template('register_page.html')


@app.route('/searchpage', methods=['GET', 'POST'])
def searchpage():

    if request.method == "POST" and request.form['searchfor']:
        searchfor = request.form['searchfor']
        session["search_for"] = searchfor
        print("in session search_for filled")
        result = Product_Information.Get_Product_By_Tag(searchfor)
        print(result, flush=True)
        session["result"] = result
        array_art = Product_Information.Get_Product_By_Category_If_Valid(
            result, '%Art%')
        session["array_art"] = array_art
        array_acc = Product_Information.Get_Product_By_Category_If_Valid(
            result, '%Accessories%')
        session["array_acc"] = array_acc
        array_com = Product_Information.Get_Product_By_Category_If_Valid(
            result, '%Comics%')
        session["array_com"] = array_com
        array_trading = Product_Information.Get_Product_By_Category_If_Valid(
            result, '%Trading Card%')
        session["array_trading"] = array_trading
        array_toys_and_models = Product_Information.Get_Product_By_Category_If_Valid(
            result, '%Toys & Models%')
        session["array_toys_and_models"] = array_toys_and_models
        return render_template('searchpage.html', result=result, array_art=array_art, array_acc=array_acc, array_com=array_com, array_trading=array_trading, array_toys_and_models=array_toys_and_models)
    if request.method == "POST":
        result = session["result"]
        i = 0

        subcategory = request.form.getlist('sub_check')
        for s in subcategory:
            new_result = ()
            subcat = s.split('-')[1]
            for r in result:
                new_result = new_result + \
                    tuple(Product_Information.Get_Product_By_SubCategory(
                        subcat, r[1]))

        print(len(new_result))

        array_art = Product_Information.Get_Product_By_Category_If_Valid(
            new_result, '%Art%')
        session["array_art"] = array_art
        array_acc = Product_Information.Get_Product_By_Category_If_Valid(
            new_result, '%Accessories%')
        session["array_acc"] = array_acc
        array_com = Product_Information.Get_Product_By_Category_If_Valid(
            new_result, '%Comics%')
        session["array_com"] = array_com
        array_trading = Product_Information.Get_Product_By_Category_If_Valid(
            new_result, '%Trading Card%')
        session["array_trading"] = array_trading
        array_toys_and_models = Product_Information.Get_Product_By_Category_If_Valid(
            new_result, '%Toys & Models%')
        session["array_toys_and_models"] = array_toys_and_models

        # Remove Session search,array_art,... from having values

        return render_template('searchpage.html', result=new_result, array_art=array_art, array_acc=array_acc, array_com=array_com, array_trading=array_trading, array_toys_and_models=array_toys_and_models)

    result = Product_Information.Get_Product_By_Tag(session["search_for"])
    session["search_for"] = result
    # This line was causing problem as I was using session["result"] to get the result that they previously entered specifically when they clicked refreshed button so I can just query through that.
    session["result"] = result
    array_art = Product_Information.Get_Product_By_Category_If_Valid(
        result, '%Art%')
    session["array_art"] = array_art
    array_acc = Product_Information.Get_Product_By_Category_If_Valid(
        result, '%Accessories%')
    session["array_acc"] = array_art
    array_com = Product_Information.Get_Product_By_Category_If_Valid(
        result, '%Comics%')
    session["array_com"] = array_com
    array_trading = Product_Information.Get_Product_By_Category_If_Valid(
        result, '%Trading Card%')
    session["array_trading"] = array_trading
    array_toys_and_models = Product_Information.Get_Product_By_Category_If_Valid(
        result, '%Toys & Models%')
    session["array_toys_and_models"] = array_toys_and_models
    return render_template('searchpage.html', result=result, array_art=array_art, array_acc=array_acc, array_com=array_com, array_trading=array_trading, array_toys_and_models=array_toys_and_models)


@app.route('/createListing', methods=['GET', 'POST'])
def createListing():

    if request.method == 'POST':

        catagory = request.form['listingCategory']
        subcatagory = request.form['listingCategory']
        print(catagory, flush=True)
        list_of_tags = request.form.getlist('boxes')
        title = request.form['title']
        print(title)
        description = request.form['desc']
        description.replace(",", "|$|")
        image = request.form['image']
        dollar = request.form['dollar']
        cent = request.form['cent']
        price = dollar + cent
        print(price)
        quantity = request.form['quantity']
        Product_Information.Insert_New_Product(list_of_tags, title, description,
                                               image, price, quantity, catagory, subcatagory)
        return redirect(url_for('homepage'))

    return render_template('Create_Listing.html')


@app.route('/itempage/<iteminfo>', methods=['GET', 'POST'])
def itempage(iteminfo):
    # Product_Information.strArrayToArray(iteminfo)
    result = Product_Information.strArrayToArray(iteminfo)
    result[5] = result[5].replace('|$|', ",")
    Buyer = session.get("UID")
    seller = result[4]
    user = SQL_Queries.UserIdToUsername(int(seller))

    shopcart = Shopping_Cart.Pull_Cart(Buyer)
    itemcount = len(shopcart)
    subtotal = 10
    return render_template('item_page.html', result=result, user=user, itemcount=itemcount, subtotal=subtotal)


@app.route('/shoppingCart')
def ShoppingCart():

    user = session.get("UID")
    Cart = Shopping_Cart.Pull_Cart(user)
    Filled = Shopping_Cart.Get_Shopping_Products(Cart)
    length = len(Filled)
    total = Shopping_Cart.Total_Shopping_Cart(Cart)
    Tax_Value = round(total * 0.0825, 2)
    Tax = ("TAX 8.25%", Tax_Value, "TAX")
    Shipping = ("SHIPPING 5.89 per Item", length * 5.89, "SHIPPING")
    T_Total = round(total + Tax_Value + Shipping[1], 2)
    irreplaceable = [Tax, Shipping]
    Checkout_Detail = SQL_Queries.Get_User_Checkout(user)

    return render_template('shopping_cart.html',
                           Tuple_List=Filled,
                           Tuple_Two=irreplaceable,
                           N_Items=length,
                           Sub_Total=total,
                           Taxed_Total=T_Total,
                           Address=Checkout_Detail[0],
                           Full_Name="{} {}".format(Checkout_Detail[1], Checkout_Detail[2]))


app.run(debug=True)
