from PY_Files import Create_User, Login_User, CONSTANTS, SQL_Queries, Product_Information, Shopping_Cart, Transaction
import re
from re import A
import sys
import os
from ast import literal_eval

# password: passwordtodb123!

import mysql.connector
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, session, flash
# from sympy import Q

tag_dictionary = {'art-ANIME': 'Anime', 'art-CARTOONS': 'Cartoons', 'art-Movies': 'Movies',
                  'art-TV': 'Television', 'art-OTHER': 'Other', 'art-CN': 'Cartoon Network',
                  'art-DC': 'DC Universe', 'art-DISNEY': 'Disney', 'art-GOT': 'Game of Thrones',
                  'art-GHOSTBUSTERS': 'Ghostbusters', 'art-HARRY': 'Harry Potter', 'art-LOTR': 'Lord of the Rings',
                  'art-MARVEL': 'Marvel', 'art-NICKELODEON': 'Nickelodeon', 'art-Nintendo': 'Nintendo',
                  'art-PIXAR': 'Pixar', 'art-POKEMON': 'Pokemon', 'art-POWER': 'Power Rangers',
                  'art-SEGA': 'SEGA', 'art-STAR-TREK': 'Star Trek', 'art-STAR-WARS': 'Star Wars',
                  'acc-ANIME': 'Anime', 'acc-CARTOONS': 'Cartoons', 'acc-Movies': 'Movies',
                  'acc-TV': 'Television', 'acc-OTHER': 'Other', 'acc-CN': 'Cartoon Network',
                  'acc-DC': 'DC Universe', 'acc-DISNEY': 'Disney', 'acc-GOT': 'Game of Thrones',
                  'acc-GHOSTBUSTERS': 'Ghostbusters', 'acc-HARRY': 'Harry Potter', 'acc-LOTR': 'Lord of the Rings',
                  'acc-MARVEL': 'Marvel', 'acc-NICKELODEON': 'Nickelodeon', 'acc-Nintendo': 'Nintendo',
                  'acc-PIXAR': 'Pixar', 'acc-POKEMON': 'Pokemon', 'acc-POWER': 'Power Rangers',
                  'acc-SEGA': 'SEGA', 'acc-STAR-TREK': 'Star Trek', 'acc-STAR-WARS': 'Star Wars',
                  'jewelry-BRACELETS': 'Bracelets', 'jewlery-EARRINGS': 'Earrings', 'jewlery-NECKLACES': 'Necklaces', 'jewelry-RINGS': 'Rings',
                  'comic-SINGLE': 'Single Issue', 'comic-OGN': 'Original Graphic Novel/Volume', 'comic-MAGAZINE': 'Magazine/Anthonlogy',
                  'comic-PAPERBACK': 'Paper Back Edition', 'comic-HARD-COVER': 'Hard Cover Edition', 'comic-DIGEST': 'Digest', 'comic-ARCHIE': 'Archie Comics',
                  'comic-BOOM': 'Boom! Studios', 'comic-DARK': 'Dark Horse', 'comic-DC': 'DC', 'comic-DEL-REY': 'Del Rey', 'comic-DYNAMITE': 'Dynamite',
                  'comic-IDW': 'IDW', 'comic-IMAGE': 'Image', 'comic-KODANSHA': 'Kodansha', 'comic-MARVEL': 'Marvel', 'comic-ONI': 'Oni Press',
                  'comic-SHOGAKUGAN': 'Shogakugan', 'comic-SHUEISHA': 'Shueisha', 'comic-TOKYOPOP': 'Tokyopop', 'comic-VALIANT': 'Valiant', 'comic-OTHER': 'Other'}

# Add the rest of the tags from create_listing.html to allow createListing function to properly insert the tags into database


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

        return redirect(url_for('searchpage'))

    ################################################################################################
    # Call function to perform SQL Query on specified categories (returns array containing tuples) #
    #
    art_products = Product_Information.Get_Product_By_Catagory(
        'Art')                                                #
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

        flash(Flash_Statement)
        if Flash_Code == 0:
            return redirect(url_for('homepage'))

    return render_template('register_page.html')


@app.route('/searchpage', methods=['GET', 'POST'])
def searchpage():

    if request.method == "POST" and request.form['searchfor']:
        searchfor = request.form['searchfor']
        session["search_for"] = searchfor

        result = Product_Information.Get_Product_By_Tag(searchfor)
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
    tags = ""
    if request.method == 'POST':

        catagory = request.form['listingCategory']
        subcatagory = request.form['listingCategory']
        uid = session["UID"]
        list_of_tags = request.form.getlist('boxes')
        title = request.form['title']

        for x in list_of_tags:
            for y in tag_dictionary:
                if x == y:
                    tags = tags + ", " + tag_dictionary[y]

        print(title)
        description = request.form['desc']
        description.replace(",", "|$|")
        image = request.form['image']
        image = image.split(".")
        dollar = request.form['dollar']
        cent = request.form['cent']
        price = dollar + cent

        quantity = request.form['quantity']
        Product_Information.Insert_New_Product(
            uid, tags, title, description, image[0], price, quantity, catagory, subcatagory)
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


@app.route('/shoppingCart', methods=['GET', 'POST'])
def ShoppingCart():

    User = session.get("UID")
    Cart = Shopping_Cart.Pull_Cart(User)

    Filled = Shopping_Cart.Get_Shopping_Products(Cart)

    length = Shopping_Cart.Cart_Length(Filled)
    total = Shopping_Cart.Total_Shopping_Cart(Filled)

    Tax_Value = round(total * 0.0825, 2)
    Tax = ("TAX 8.25%", Tax_Value, "TAX")
    Shipping = ("SHIPPING 5.89 per Item", length * 5.89, "SHIPPING")
    T_Total = round(total + Tax_Value + Shipping[1], 2)
    irreplaceable = [Tax, Shipping]
    Checkout_Detail = SQL_Queries.Get_User_Checkout(User)

    if request.method == "POST" and request.form.getlist('Delete_Checks'):
        print("POSTER!")
        Deleter_List = request.form.getlist('Delete_Checks')
        print(Deleter_List)
        
        
        Deleter_List = Shopping_Cart.Get_PID_From_P_Name(Deleter_List)

    if request.method == "POST":
        print("Posted!")
        Shipping = Transaction.Make_Address_String(request.form["shipAddr"],
                                                   request.form["shipState"],
                                                   request.form["shipCity"],
                                                   request.form["shipZip"],
                                                   request.form["shipApt"])
        print(Shipping)
        if request.form.get("billzor"):
            Billing = Transaction.Make_Address_String(
                request.form["billAddr"],
                request.form["billState"],
                request.form["billCity"],
                request.form["billZip"],
                request.form["billApt"])
        else:
            Billing = Shipping

        Transaction.Create_Transaction_Tuple(       UID=User,
                                                     Cart_IDs=str(Cart),
                                                     Cart_Names=Transaction.Make_Cart_Names(
                                                         Filled),
                                                     Taxed_Total=T_Total,
                                                     Date=Transaction.Get_Date(),
                                                     Payment_Info=Transaction.Redact_CC(
                                                         request.form["cardNumber"]),
                                                     S_Address=Shipping,
                                                     B_Address=Billing)
        Shopping_Cart.Empty_Cart(User)


    return render_template('shopping_cart.html',
                           Tuple_List=Filled,
                           Tuple_Two=irreplaceable,
                           N_Items=length,
                           Sub_Total=total,
                           Taxed_Total=T_Total,
                           Address=Checkout_Detail[0],
                           Full_Name="{} {}".format(Checkout_Detail[1], Checkout_Detail[2]))


app.run(debug=True)
