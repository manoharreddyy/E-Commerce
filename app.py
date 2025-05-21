from flask import Flask, render_template, request
import pymysql
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'ECOM'
}

@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register1")
def register1():
    return render_template("register.html")

@app.route("/register2", methods=['POST','GET'])
def register2():
    fullname = request.form['fullname']
    email = request.form['email']
    mobile = request.form['mobile']
    password = request.form['password']
    confirmpassword = request.form['confirm-password']

    # checking for duplicates
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USER WHERE FULLNAME = %s"
    cursor.execute(query, (fullname,))
    data = cursor.fetchone()
    conn.close()

    if data is not None:
        return render_template("register.html", msg="usernameexist")
    elif password != confirmpassword:
        return render_template("register.html", msg="wrongpassword")
    else:
        otp = random.randint(1111, 9999)
        body = f"OTP for validation: {otp}"

        msg = MIMEMultipart()
        msg["From"] = "kodudhulapoojitha19@gmail.com"
        msg["To"] = email
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("kodudhulapoojitha19@gmail.com", "pwvf bodv idoa ubcl")
        server.send_message(msg)
        server.quit()

        return render_template("otpverification.html", fullname=fullname, email=email, mobile=mobile, password=password, otp=otp)

@app.route("/register3", methods=['POST','GET'])
def register3():
    fullname = request.form['fullname']
    email = request.form['email']
    mobile = request.form['mobile']
    password = request.form['password']
    otp = request.form['otp']
    cotp = request.form['cotp']

    if str(otp) != str(cotp):
        newotp = random.randint(1111, 9999)
        body = f"OTP for validation: {newotp}"

        msg = MIMEMultipart()
        msg["From"] = "kodudhulapoojitha19@gmail.com"
        msg["To"] = email
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("kodudhulapoojitha19@gmail.com", "pwvf bodv idoa ubcl")
        server.send_message(msg)
        server.quit()

        return render_template("otpverification.html", msg="invalid", fullname=fullname, email=email, mobile=mobile, password=password, otp=newotp)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO USER VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(fullname,email,mobile,password))
        conn.commit()
        conn.close()
        return render_template("login.html", msg="accountcreated")
    
@app.route("/login1")
def login():
    return render_template("login.html")

@app.route("/login2",methods = ['POST','GET'])
def login2():
    fullname = request.form['fullname']
    password = request.form['password']

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USER WHERE FULLNAME = %s"
    cursor.execute(query,(fullname))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return render_template("login.html",msg="nouser")
    if data[-1] != password:
        return render_template("login.html",msg="wrongpassword")
    else:
        return render_template("user_home.html", fullname=fullname)
    
@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgotpassword1.html")

@app.route("/forgotpassword1",methods=["POST","GET"])
def forgotpassword1():
    fullname = request.form["fullname"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USER WHERE FULLNAME = %s"
    cursor.execute(query,(fullname,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        return render_template("forgotpassword1.html",msg="nouser")
    else:
        newotp = random.randint(1111,9999)

        body = f"OTP For Validation is {newotp}"
    
        msg = MIMEMultipart()
        msg["From"] = "kodudhulapoojitha19@gmail.com"
        msg["To"] = data[1]
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("kodudhulapoojitha19@gmail.com","pwvf bodv idoa ubcl")
        server.send_message(msg)
        server.quit()

        return render_template("forgotpassword2.html",username=data[0],email=data[1],otp=newotp)
    
@app.route("/forgotpassword2",methods=["POST","GET"])
def forgotpassword2():
    fullname = request.form["fullname"]
    email = request.form["email"]
    otp = request.form["otp"]
    cotp = request.form["cotp"]
    password = request.form["password"]
    cpassword = request.form["cpassword"]
    print(fullname)
    print(email)
    print(otp)
    print(cotp)
    print(password)
    print(cpassword)
    
    if str(otp) != str(cotp):
        newotp = random.randint(1111,9999)

        body = f"OTP For Validation is {newotp}"
    
        msg = MIMEMultipart()
        msg["From"] = "kodudhulapoojitha19@gmail.com"
        msg["To"] = email
        msg["Subject"] = "OTP For Validation"
        msg.attach(MIMEText(body,'plain'))

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("kodudhulapoojitha19@gmail.com","pwvf bodv idoa ubcl")
        server.send_message(msg)
        server.quit()

        return render_template("forgotpassword2.html",msg="wrongotp",fullname=fullname,email=email,otp=newotp)
    elif password != cpassword:
        return render_template("forgotpassword3.html",msg="wrongpassword",fullname=fullname,email=email)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE USER SET PASSWORD = %s WHERE FULLNAME = %s"
        cursor.execute(query,(password,fullname))
        conn.commit()
        conn.close()
        return render_template("login.html",msg="passwordreset")
@app.route("/forgotpassword3",methods=["POST","GET"])
def forgotpassword3():
    fullname = request.form["fullname"]
    email = request.form["email"]
    password = request.form["password"]
    cpassword = request.form["cpassword"]
    print(fullname)
    print(email)
    print(password)
    print(cpassword)

    if password != cpassword:
        return render_template("forgotpassword3.html",msg="wrongpassword",fullname=fullname,email=email)
    else:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE USER SET PASSWORD = %s WHERE FULLNAME = %s"
        cursor.execute(query,(password,fullname))
        conn.commit()
        conn.close()
        return render_template("login.html",msg="passwordreset")
    
@app.route("/addtocart1", methods = ["POST","GET"])
def addtocart1():
    fullname = request.form["fullname"]
    product_id = request.form["productid"]
    product_name = request.form["productname"]
    product_price = request.form["productprice"]
    print(fullname)
    print(product_id)
    print(product_name)
    print(product_price)
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE FULLNAME = %s AND PRODUCT_ID = %s"
    cursor.execute(query,(fullname,product_id))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO CART (fullname, product_id, product_name, product_price) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(fullname,product_id,product_name,product_price))
        conn.commit()
        conn.close()
        return render_template("user_home.html",fullname=fullname,msg="p1")
    else:
        qty = int(data[-1])+1
        price = int(data[-2])*qty
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE CART SET QUANTITY = %s WHERE PRODUCT_ID = %s AND FULLNAME = %s"
        cursor.execute(query,(qty,product_id,fullname))
        conn.commit()
        conn.close()

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE CART SET PRODUCT_PRICE = %s WHERE PRODUCT_ID = %s AND FULLNAME = %s"
        cursor.execute(query,(price,product_id,fullname))
        conn.commit()
        conn.close()
        return render_template("user_home.html",fullname=fullname, msg="p2")
    
@app.route("/shoppingcart/<fullname>")
def shoppingcart(fullname):

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE FULLNAME=%s"
    cursor.execute(query,(fullname,))
    data = cursor.fetchall()
    conn.close()
    print(data)

    if len(data) == 0:
        return render_template("user_home.html",fullname=fullname,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total+=int(i[-2])
        return render_template("cart.html",data = data, fullname=fullname,grandtotal=total)
    
@app.route("/user_home2/<fullname>")
def user_home2(fullname):
    return render_template("user_home.html",fullname=fullname)

@app.route("/deleteproduct/<pid>/<fullname>")
def deleteproduct(pid,fullname):

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM CART WHERE PRODUCT_ID=%s"
    cursor.execute(query,(pid,))
    conn.commit()
    conn.close()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE FULLNAME=%s"
    cursor.execute(query,(fullname,))
    data = cursor.fetchall()
    conn.close()
    print(data)

    if len(data) == 0:
        return render_template("user_home.html",fullname=fullname,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total+=int(i[-2])
        return render_template("cart.html",data = data, fullname=fullname,grandtotal=total)
    
    
@app.route("/success",methods=["POST","GET"])
def success():
    fullname = request.form["fullname"]

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO ORDERS (FULLNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE,QUANTITY) SELECT FULLNAME,PRODUCT_ID,PRODUCT_NAME,PRODUCT_PRICE,QUANTITY FROM CART"
    cursor.execute(query,)
    conn.commit()
    conn.close()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM CART WHERE FULLNAME = %s"
    cursor.execute(query,(fullname,))
    conn.commit()
    conn.close()
    return render_template("user_home.html",fullname=fullname)

@app.route("/failure",methods=["POST","GET"])
def failure():
    fullname = request.form["fullname"]
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM CART WHERE FULLNAME = %s"
    cursor.execute(query,(fullname))
    data = cursor.fetchall()
    conn.close()
   
    if len(data) == 0:
        return render_template("user_home.html",fullname=fullname,msg="noproductsincart")
    else:
        total = 0
        for i in data:
            total += int(i[-2])
        return render_template("cart.html",data=data,fullname=fullname,grandtotal=total)

@app.route("/orders/<fullname>")
def orders(fullname):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM ORDERS WHERE FULLNAME = %s"
    cursor.execute(query,(fullname))
    data = cursor.fetchall()
    conn.close()
    return render_template("orders.html",data=data,fullname=fullname)



app.run(port=5015)
