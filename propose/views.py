from email import message
from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail
import random
import mysql.connector

# Create your views here.

def register(request):
    roll = request.POST.get("roll", "")
    password = request.POST.get("password", "")
    msg=''
    # mydb = mysql.connector.connect(host="sql12.freemysqlhosting.net",user="sql12593693",password="2nytQApMNx",charset='utf8',database="sql12593693")
    mydb = mysql.connector.connect(host="bsqx344asdfmrehlcqd5-mysql.services.clever-cloud.com",user="ugvj28luz0jwzcjf",password="wvzQGiU131HkHzJ8nhr6",charset='utf8',database="bsqx344asdfmrehlcqd5")
    if(roll!=""):
        code = random.randint(1111,9999)
        message = "Verification code : " + str(code)
        cursor=mydb.cursor()
        cursor.execute('SELECT * FROM accounts WHERE roll = %s', (roll,))
        account = cursor.fetchone()
        if account:
            if(account[4]!=""):
                msg="Account already Active"
            else:
                cursor.execute('UPDATE accounts SET password = %s WHERE roll = %s', (password, roll,))
                mydb.commit()
                send_mail("Verification", message, "valentinehncc@gmail.com", [account[1]], fail_silently=False,)
                print(code)
                request.session["code"]=code
                request.session["mail"]=account[1]
                request.session["roll"]=roll
                return redirect("verify")
        else:
            msg="Incorrect Roll Number"
    param ={"msg":msg}
    mydb.close()
    return render(request, "register.html",param)

def verify(request):
    # mydb = mysql.connector.connect(host="sql12.freemysqlhosting.net",user="sql12593693",password="2nytQApMNx",charset='utf8',database="sql12593693")
    mydb = mysql.connector.connect(host="bsqx344asdfmrehlcqd5-mysql.services.clever-cloud.com",user="ugvj28luz0jwzcjf",password="wvzQGiU131HkHzJ8nhr6",charset='utf8',database="bsqx344asdfmrehlcqd5")
    try:
        code=request.session["code"]
    except:
        return redirect("register")
    code = request.POST.get("code", "")
    msg=''
    if(code!=""):
        if(int(code)!=request.session["code"]):
            print(code, request.session["code"])
            msg="Incorrect Code"
        else:
            cursor=mydb.cursor()
            cursor.execute('UPDATE accounts SET state = "Active", status = "verified" WHERE roll = %s', (request.session["roll"],))
            mydb.commit()
            return redirect("register")
    param={"msg":msg}
    mydb.close()
    return render(request, "verify.html", param)

def login(request):
    roll = request.POST.get("roll", "")
    password = request.POST.get("password", "")
    msg=''
    # mydb = mysql.connector.connect(host="sql12.freemysqlhosting.net",user="sql12593693",password="2nytQApMNx",charset='utf8',database="sql12593693")
    mydb = mysql.connector.connect(host="bsqx344asdfmrehlcqd5-mysql.services.clever-cloud.com",user="ugvj28luz0jwzcjf",password="wvzQGiU131HkHzJ8nhr6",charset='utf8',database="bsqx344asdfmrehlcqd5")
    if(roll!=""):
        cursor=mydb.cursor()
        cursor.execute('SELECT * FROM accounts WHERE roll = %s', (roll,))
        account = cursor.fetchone()
        if account:
            if(account[4]==""):
                msg="Account is Incative!!!"
            elif(password!=account[6]):
                msg="Incorrect Password!!!"
            else:
                return redirect("home")
        else:
            msg="Incorrect Roll Number"
    param ={"msg":msg}
    mydb.close()
    return render(request, "login.html",param)

def home(request):
    return render(request, "home.html")