from flask import  Flask,render_template, request, redirect, url_for, session
import ibm_db
import os
from dotenv import load_dotenv
import pandas as pd
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Loading up the values
load_dotenv()
#DB Creds
database = os.environ.get("DATABASE")
db_hostname = os.environ.get("HOSTNAME")
db_port = os.environ.get("PORT")
db_uid = os.environ.get("UID")
db_pwd = os.environ.get("PWD")
email_pwd = os.environ.get("email_password")

# Database Connection
try:
    conn = ibm_db.connect(
    f'DATABASE={database};HOSTNAME={db_hostname};PORT={db_port};SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID={db_uid};PWD={db_pwd}', '', '')
    print("Connected to database: ", conn)
except Exception as e:
    print (e)

# Home Route
@app.route('/',methods = ['POST', 'GET'])
def home():

    def send_mail(r_mail, content):
        s_mail = "yeskay2302@gmail.com"
        s_pass = email_pwd
        msg=EmailMessage()
        msg['Subject'] = f"Registration Successful"
        msg['From'] = s_mail
        msg['To'] = r_mail
        msg.set_content(content,subtype="html")

        server = smtplib.SMTP_SSL("smtp.gmail.com",465)

        try:
            server.login(s_mail,s_pass)
            print("Logged In Successfully")
            server.send_message(msg)
            print("Mail Sent")
            server.quit()
        except Exception as e:
            print(e)

    if request.method == 'POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        print(first_name, last_name, email, password, confirm_password)

        if(password==confirm_password):
            sql = "SELECT * FROM users WHERE email = '"+email+"' "
            print(sql)
            stmt = ibm_db.exec_immediate(conn, sql)
            
            account = ibm_db.fetch_assoc(stmt)
            print(account)

            if account:
                print("User already exists")
                return render_template('register.html', msg="User already exists, Please login")
            else:
                print("User does not exist")
                try:
                    insert_query = "INSERT INTO users VALUES('"+email+"','"+password+"','"+first_name+"','"+last_name+"')"
                    ibm_db.exec_immediate(conn, insert_query)
                    print("You are successfully registered")
                    with open('mail.html', 'r') as f:
                        mail_content= f.read()
                        send_mail(email, mail_content)
                    return render_template('login.html')
                    
                except Exception as e:
                    print(e)
                
                
        else:
            print("Password does not match")
            return render_template('register.html', msg="Password does not match")
        

    return render_template('register.html',title="Register")

@app.route('/login',methods = ['POST', 'GET'])
def login():
    
    return render_template('login.html', msg="User exists, Sprint 1 Completed")

if __name__ == "main":
    app. run(debug=True, use_reloader=True)
    