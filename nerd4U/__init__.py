import re
from re import A
import sys
import os
from ast import literal_eval

#password: passwordtodb123!

import mysql.connector
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, session, flash
from werkzeug.utils import secure_filename




tag_dictionary = {'art-ANIME': 'Anime','art-CARTOONS': 'Cartoons', 'art-Movies': 'Movies',
                  'art-TV': 'Television', 'art-OTHER': 'Other', 'art-CN': 'Cartoon Network',
                  'art-DC': 'DC Universe', 'art-DISNEY': 'Disney', 'art-GOT': 'Game of Thrones',
                  'art-GHOSTBUSTERS': 'Ghostbusters', 'art-HARRY': 'Harry Potter', 'art-LOTR': 'Lord of the Rings',
                  'art-MARVEL': 'Marvel', 'art-NICKELODEON': 'Nickelodeon', 'art-Nintendo': 'Nintendo',
                  'art-PIXAR': 'Pixar', 'art-POKEMON': 'Pokemon', 'art-POWER': 'Power Rangers',
                  'art-SEGA': 'SEGA', 'art-STAR-TREK': 'Star Trek', 'art-STAR-WARS': 'Star Wars',
                  'acc-ANIME': 'Anime','acc-CARTOONS': 'Cartoons', 'acc-Movies': 'Movies',
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
sys.path.insert(1, 'nerd4U/PY_Files')

from PY_Files import Create_User, Login_User, CONSTANTS, SQL_Queries, Product_Information, Shopping_Cart, Transaction


app = Flask(__name__)

app.secret_key = 'super secret key'

# Connect to database

DB = mysql.connector.connect(user="jtmoney", password="HelpHimRnPlz1327!", host="nerd4u-ecommerce-database.mysql.database.azure.com", port=3306, database="nerd4u")

allowed_extensions = set(['png','jpg','jpeg'])

def allowed_file(file_name):
    return '.' in file_name and file_name.rsplit('.',1)[1].lower() in allowed_extensions

## Home Page ##
@app.route('/', methods=['GET', 'POST'])
def homepage():


    # Grab what user enters in searchpage and use it to fill searchpage.html #
    if request.method == 'POST':
        search_for = request.form['search_bar']
        session["search_for"] = search_for
        return redirect(url_for('searchpage'))

    ################################################################################################
    # Call function to perform SQL Query on specified categories (returns array containing tuples) #
        #
    art_products = Product_Information.Get_Product_By_Catagory(
         'Art')                              #
    comic_products = Product_Information.Get_Product_By_Catagory(
        'Comics')                         #
    toy_products = Product_Information.Get_Product_By_Catagory(
        'Toys & Models')                    #

    #####################################################################################
    # Recurse through each tuple, only returning the third data column (the image id's) #
    #####################################################################################
    #                                                                #
    art_img_ids = (tuple(map(lambda x: x[3], art_products)))
    comic_img_ids = (
        tuple(map(lambda x: x[3], comic_products)))                        #
    #
    toy_img_ids = (tuple(map(lambda x: x[3], toy_products)))

    return render_template('homepage.html',
                           art_img_ids=art_img_ids,
                           comic_img_ids=comic_img_ids,
                           toy_img_ids=toy_img_ids,
                           
                           comic_products=comic_products,
                           toy_products=toy_products
                           )  # Display's homepage when at root directory of website along with all products ##

## Art Page ##
@app.route('/artPage')
def artpage():

    # Grab what user enters in searchpage and use it to fill searchpage.html #
    if request.method == 'POST':
        search_for = request.form['search_bar']
        session["search_for"] = search_for    
        return redirect(url_for('searchpage'))

    ###################################################################################################
    # Call function to perform SQL Query on specified subcategories (returns array containing tuples) #
    ###################################################################################################                                                                                                  
    art_products = Product_Information.Get_Product_By_Catagory('Art')                                 #
    art_draw_paint = Product_Information.Get_Product_By_SubCategory_Only('Drawing & Painting')             #
    art_mixed_media = Product_Information.Get_Product_By_SubCategory_Only('Mixed Media')                   #
    art_print_photo = Product_Information.Get_Product_By_SubCategory_Only('Prints & Photography')          #
    art_sculptures = Product_Information.Get_Product_By_SubCategory_Only('Sculptures')                     #

    ############################################################################
    #           Return the art page with all of it's subcategories             #
    ############################################################################
    return render_template('artPage.html',                                    #
                           art_products=art_products,                          #
                           art_draw_paint = art_draw_paint,                    #
                           art_mixed_media = art_mixed_media,                  #
                           art_print_photo = art_print_photo,                  #
                           art_sculptures = art_sculptures                     #
                           )                                                   #

@app.route('/upload/<filename>')
def send_image(filename):

    # Send the image the html page has requested to display on html page #
    print(send_from_directory("../Images", filename))
    return send_from_directory("../Images", filename)


## User Login Page ##

@app.route('/userLogin', methods=['GET', 'POST'])
def login():
    ## Login for auto fill ## 
    if request.form.get("autoFill") and (request.form.get("adminAcc") == None):
        if request.method == 'POST':
            username="Andy"  
            passw="Marvin"
            account=Login_User.Login_User(username,passw)
            print(account)
            # if account == 'none':
            #     flash('Incorrect User information')
            #     return render_template('login.html')
            
            
            session["UID"] = str(account)
            session["username"] = username
            flash('Login Sucessful. Welcome back ' +  username + '!')
            return redirect(url_for('homepage'))

    if request.form.get("adminAcc") and (request.form.get("autoFill") == None):
        if request.method == 'POST':
            username="admin"  
            passw="password"
            account=Login_User.Login_User(username,passw)
            print(account)
            if account == 'none':
                flash('Incorrect User information')
                return render_template('login.html')
            
            else:
                session["UID"] = str(account)
                session["username"] = username
                flash('Login Sucessful. Welcome back ' +  username + '!')
                return redirect(url_for('homepage'))

    ## Login for Auto Fill Admin account ##

    ## Login for manual login ##
    if session.get("UID") == None or session['UID'] == '00':
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            passw = request.form['password']
            account = Login_User.Login_User(username,passw)
            print(account)
            if account == 'none':
                flash('Incorrect User information')
                return render_template('login.html')
            
            else:
                session["UID"] = str(account)
                session["username"] = username
                flash('Login Sucessful. Welcome back ' +  username + '!')
                return redirect(url_for('homepage'))
                
        # Show the login form with message (if any)

        return render_template('login.html')

    if session["username"]=='admin': 
                return redirect(url_for('adminPage'))


    else:
        return redirect(url_for('accountpage'))

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
    list=[]
    
    if request.method == "POST" and request.form['searchfor']:
        searchfor = request.form['searchfor']
        session["search_for"] = searchfor
        result = Product_Information.Get_Product_By_Tag(searchfor)
        session["result"] = result
        array_art = Product_Information.Get_Product_By_Category_If_Valid(result, '%Art%')
        session["array_art"] = array_art
        array_acc = Product_Information.Get_Product_By_Category_If_Valid(result, '%Accessories%')
        session["array_acc"] = array_acc
        array_com = Product_Information.Get_Product_By_Category_If_Valid(result, '%Comics%')
        session["array_com"] = array_com
        array_trading = Product_Information.Get_Product_By_Category_If_Valid(result, '%Trading Card%')
        session["array_trading"] = array_trading 
        array_toys_and_models = Product_Information.Get_Product_By_Category_If_Valid(result, '%Toys & Models%')
        session["array_toys_and_models"] = array_toys_and_models
        return render_template('searchpage.html', result = result
                                                , array_art = array_art
                                                , array_acc = array_acc
                                                , array_com = array_com
                                                , array_trading = array_trading
                                                , array_toys_and_models = array_toys_and_models)
    if request.method == "POST":

        array_art = None
        array_acc = None
        array_com = None
        array_trading = None 
        array_toys_and_models = None
        array_art_valid = False
        array_acc_valid = False
        array_com_valid = False
        array_trading_valid = False 
        array_toys_and_models_valid = False
        result = session["result"]
        result = (result)
        new_result = []

        i=0
        subcategory = request.form.getlist('sub_check')

        subcategories_displayed=[]
        i=0
        # for res in result:
        #     subcategories_displayed.insert(i,res[9])
        #     i+=1
        # unique_subcategories_displayed = set(subcategories_displayed)
        # print(unique_subcategories_displayed)

        for s in subcategory:
            i=0
            subcat = s
            print(s)
            for r in result:
                result_r = r[9].split(' ')
                if result_r[0] == subcat:
                    print(result_r[0],subcat)

                    new_result.insert(i,r)
                    i+=1

                    if r[8] == "Art":
                        array_art_valid=True
                    if r[8] == "Accessories":
                        array_acc_valid=True
                    if r[8] == "Comics":
                        array_com_valid=True
                    if r[8] == "Trading Cards":
                        array_trading_valid=True
                    if r[8] == "Toys & Models":
                        array_toys_and_models_valid=True
                
                
        print(array_acc_valid,array_com_valid,array_acc_valid, array_trading_valid,array_toys_and_models_valid)
        if (array_art_valid == True):
            array_art = Product_Information.Get_Product_By_Category_If_Valid(new_result, '%Art%')
            session["array_art"] = array_art
        if (array_acc_valid == True):
            array_acc = Product_Information.Get_Product_By_Category_If_Valid(new_result, '%Accessories%')
            session["array_acc"] = array_acc
        if (array_com_valid == True):
            array_com = Product_Information.Get_Product_By_Category_If_Valid(new_result, '%Comics%')
            session["array_com"] = array_com
        if (array_trading_valid == True):
            array_trading = Product_Information.Get_Product_By_Category_If_Valid(new_result, '%Trading Card%')
            session["array_trading"] = array_trading 
        if (array_toys_and_models_valid == True):
            array_toys_and_models = Product_Information.Get_Product_By_Category_If_Valid(new_result, '%Toys & Models%')
            session["array_toys_and_models"] = array_toys_and_models

        # Remove Session search,array_art,... from having values

        return render_template('searchpage.html', result = new_result
                                                , array_art = array_art
                                                , array_acc = array_acc
                                                , array_com = array_com
                                                , array_trading = array_trading
                                                , array_toys_and_models = array_toys_and_models)


    result = Product_Information.Get_Product_By_Tag(session["search_for"])


    ## This line was causing problem as I was using session["result"] to get the result that they previously entered specifically when they clicked refreshed button so I can just query through that.
    session["result"] = result
    array_art = Product_Information.Get_Product_By_Category_If_Valid(result, '%Art%')
    session["array_art"] = array_art
    array_acc = Product_Information.Get_Product_By_Category_If_Valid(result, '%Accessories%')
    session["array_acc"] = array_art
    array_com = Product_Information.Get_Product_By_Category_If_Valid(result, '%Comics%')
    session["array_com"] = array_com
    array_trading = Product_Information.Get_Product_By_Category_If_Valid(result, '%Trading Card%')
    session["array_trading"] = array_trading
    array_toys_and_models = Product_Information.Get_Product_By_Category_If_Valid(result, '%Toys & Models%')
    session["array_toys_and_models"] = array_toys_and_models
    return render_template('searchpage.html', result = result
                                            , array_art = array_art
                                            , array_acc = array_acc
                                            , array_com = array_com
                                            , array_trading = array_trading
                                            , array_toys_and_models = array_toys_and_models)
    
@app.route('/createListing', methods=['GET', 'POST'])
def createListing():    
    tags = ""
    if session.get('UID') == None:
        return redirect(url_for('login'))

    if request.method == 'POST' and session.get('UID') != None:

        catagory = request.form['listingCategory']
        subcatagory = request.form['listingCategory']
        uid = session["UID"] 
        list_of_tags = request.form.getlist('boxes')
        title = request.form['title']

        for x in list_of_tags:
            for y in tag_dictionary:
                if x == y:
                    tags = tags + ", " +tag_dictionary[y]
           

        description = request.form['desc']
        description.replace(",", "|$|")
        image = request.form['image']
        image = image.split(".")
        # print(image)

        # if 'file' not in request.files:
        #     flash('No file part')

        # file = request.files['file']
        # if file.filename == '':
        #     flash('No image selected for uploading')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     #print('upload_image filename: ' + filename)
        #     flash('Image successfully uploaded and displayed below')

        # else:
        #     flash('Allowed image types are - png, jpg, jpeg, gif')



        dollar = request.form['dollar']
        price=dollar

        quantity = request.form['quantity']
        Product_Information.Insert_New_Product(uid,tags, title, description,image[0], price, quantity,catagory, subcatagory)

        flash("You successfully created a item listing!")
        return redirect(url_for('homepage'))

    return render_template('Create_Listing.html')
@app.route('/itempage/<iteminfo>', methods=['GET','POST'])
def itempage(iteminfo):
       # Product_Information.strArrayToArray(iteminfo)

    if session.get("UID") == None or session['UID'] == '00':
        result = Product_Information.strArrayToArray(iteminfo)
        result[5] = result[5].replace('|$|', ",")
        print("THIS IS RESULT" ,result)
        uli = False
        seller = result[4]
        seller = SQL_Queries.UserIdToUsername(str(seller))
        if request.method == "POST":
            return redirect(url_for('login'))

        return render_template('item_page.html',
                        result=result,
                        user=seller,
                        user_logged_in=uli)
    else:
        uli=True
        user = session["UID"]
        Cart = Shopping_Cart.Pull_Cart(user)
        Filled = Shopping_Cart.Get_Shopping_Products(Cart)
        length = Shopping_Cart.Cart_Length(Filled)
        total = Shopping_Cart.Total_Shopping_Cart(Filled)
        result = Product_Information.strArrayToArray(iteminfo)
        
        result[5] = result[5].replace('|$|', ",")
        seller = result[4]

        seller = SQL_Queries.UserIdToUsername(str(seller))
        print("The seller is ! ", seller)
        adding_to_cart = int(total) + int(result[2])
        if request.method == "POST":

            Cart = Shopping_Cart.Add_Item(Cart,result[0])

            Shopping_Cart.Push_Cart(Cart,user)
            return redirect(url_for('ShoppingCart'))

        return render_template('item_page.html',
                            result=result,
                            user=seller,
                            itemcount=length,
                            subtotal=total,
                            adding_to_cart=adding_to_cart,
                            user_logged_in=uli)

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
        Deleter_List = request.form.getlist('Delete_Checks')
        Deleter_List = Shopping_Cart.Get_PID_From_P_Name(Deleter_List)

    if request.method == "POST":
        Shipping = Transaction.Make_Address_String(request.form["shipAddr"],
                                                   request.form["shipState"],
                                                   request.form["shipCity"],
                                                   request.form["shipZip"],
                                                   request.form["shipApt"])
        if request.form.get("billzor"):
            Billing = Transaction.Make_Address_String(
                request.form["billAddr"],
                request.form["billState"],
                request.form["billCity"],
                request.form["billZip"],
                request.form["billApt"])
        else:
            Billing = Shipping

        Transaction.Create_Transaction_Tuple(UID=User,
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
        return redirect(url_for('ShoppingCart'))


    return render_template('shopping_cart.html',
                           Tuple_List=Filled,
                           Tuple_Two=irreplaceable,
                           N_Items=length,
                           Sub_Total=total,
                           Taxed_Total=T_Total,
                           Address=Checkout_Detail[0],
                           Full_Name="{} {}".format(Checkout_Detail[1], Checkout_Detail[2]))

    UID = session
    cart = Shopping_Cart. Pull_Cart(UID)
    return render_template('shopping_cart.html')


@app.route('/accountpage', methods=['GET','POST'])
def accountpage():
    order_list=[]
    user_listings=[]
    product=[]
    listing_user=[]
    num_items=[]
    i=0
    if session['UID'] != None:

        user = SQL_Queries.UserIdToUsername(session['UID'])


        user_transactions = Transaction.Pull_Transactions_From_UID(session['UID'])

        for y in user_transactions:

            pids = y[2]
            pids = pids.strip('[]').split(', ')
            res = y[3].split(',')    
        trans = list(user_transactions)
        user_listings = Product_Information.Get_Product_By_UID(session['UID'])

        print(trans)
        for listing in user_listings:
            if int(listing[7]) > 0:
                listing_user.append(('N/A',str(listing[1]),str(listing[2]),str(listing[6]),'N','N/A'))
            else:
                listing_user.append(('N/A',str(listing[1]),str(listing[2]),str(listing[6]),'Y','N/A'))
        
        return render_template('account_page.html',user=user, order_list = trans,num_items=res, product=product, user_listings = listing_user)

@app.route('/logout',methods=['GET','POST'])
def logout():
       if request.method == "POST":

        session.pop('UID',None)
        flash("You have been logged out. We hope to see you again!")
        session["username"] = ""

        return redirect(url_for('homepage'))
        
@app.route('/adminPage',methods=['GET','POST'])
def adminPage():

    # Gather information for listings

    all_results = SQL_Queries.Get_All_Listings()
    for result in all_results:
        print(result[3])
    return render_template('admin_listings.html',listings=all_results)

@app.route('/adminOrders',methods=['GET','POST'])
def adminOrders():

    # Gather information for orders
    one=()
    i=0
    all_results = SQL_Queries.Get_All_Orders()

    for one_result in all_results:
        if len(list(one_result[2])) > 1:
            print("greater than one")
        elif len(one_result[2]) == 1:
            print("Just one")



    print(one_result[3])
    return render_template('admin_orders.html',trans=all_results)

@app.route('/adminUsers',methods=['GET','POST'])
def adminUsers():

    # Gather information for users
    all_results = SQL_Queries.Get_All_Users()
    for result in all_results:
        print(result[3])
    return render_template('admin_users.html',users=all_results)

@app.route('/updateFullName',methods=['GET','POST'])
def updateFullName():
    if request.method=="POST":
        if request.form['firstname']:
            if request.form['lastname']:
                firstname = request.form['firstname']
                lastname = request.form['lastname']

                SQL_Queries.UpdateName(str(firstname),str(lastname),str(session['UID']))
                return redirect(url_for("accountpage"))
    return render_template("accountpage.html")
@app.route('/updatePassword',methods=['GET','POST'])
def updatePassword():
    if request.method=="POST":
            current = request.form['current']
            new = request.form['new']
            confirm = request.form['confirm']

            actual = SQL_Queries.Get_Password_With_UID(session["UID"])

            if str(actual) == str(current):
                if str(new) == str(confirm):
                    SQL_Queries.UpdatePassword(str(new),str(session['UID']))
                    return redirect(url_for("accountpage"))
            else:
                return redirect(url_for("homepage"))
@app.route('/updatePhone', methods=['GET','POST'])
def updatePhone():
    if request.method=="POST":
        phone = request.form['phone']
        SQL_Queries.updatePhone(str(phone),str(session["UID"]))
        return redirect(url_for("accountpage"))
@app.route('/updateUsername', methods=['GET','POST'])
def updateUsername():
    if request.method=="POST":
        if request.form['username']:
            username = request.form['username']
            SQL_Queries.UpdateUser(str(username),str(session['UID']))
            return redirect(url_for("accountpage"))
@app.route('/updateEmail',methods=['GET','POST'])
def updateEmail():
    if request.method=="POST":
        if request.form['email']:
            email = request.form['email']
            SQL_Queries.UpdateEmail(str(email),str(session["UID"]))
            return redirect(url_for("accountpage"))

@app.route('/updateAddress', methods=['GET','POST'])
def updateAddress():
    if request.method=="POST":
        address = request.form['address']
        state = request.form['state']

        SQL_Queries.UpdateAddress(str(address),str(state),str(session["UID"]))
        return redirect(url_for("accountpage"))



app.run()