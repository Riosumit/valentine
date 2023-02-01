from email import message
from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail
import random
import mysql.connector

# Create your views here.

def register(request):
    try:
        loggedin = request.session['loggedin']
    except:
        loggedin = False
    if loggedin:
        return redirect(home)
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
            if(account[5]!=""):
                msg="Account already Active"
            else:
                cursor.execute('UPDATE accounts SET password = %s WHERE roll = %s', (password, roll,))
                mydb.commit()
                send_mail("Verification", message, "valentinehncc@gmail.com", [account[2]], fail_silently=False,)
                print(code)
                request.session["code"]=code
                request.session["mail"]=account[2]
                request.session["roll"]=roll
                return redirect("verify")
        else:
            msg="Incorrect Roll Number"
        cursor.close()
    param ={"msg":msg}
    mydb.close()
    return render(request, "register.html",param)

def verify(request):
    try:
        loggedin = request.session['loggedin']
    except:
        loggedin = False
    if loggedin:
        return redirect(home)
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
            cursor.close()
            return redirect("register")
    param={"msg":msg}
    mydb.close()
    return render(request, "verify.html", param)

def login(request):
    try:
        loggedin = request.session['loggedin']
    except:
        loggedin = False
    if loggedin:
        return redirect(home)
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
            if(account[5]==""):
                msg="Account is Incative!!!"
            elif(password!=account[7]):
                msg="Incorrect Password!!!"
            else:
                request.session["loggedin"]=True
                request.session["logged_roll"]=roll
                return redirect("home")
        else:
            msg="Incorrect Roll Number"
        cursor.close()
    param ={"msg":msg}
    mydb.close()
    return render(request, "login.html",param)

def logout(request):
    del request.session["loggedin"]
    del request.session["logged_roll"]
    return redirect("home")

def home(request):
    try:
        loggedin = request.session['loggedin']
    except:
        loggedin = False
    param = {'loggedin':loggedin}
    return render(request, "home.html", param)

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def propose(request):
    # mydb = mysql.connector.connect(host="sql12.freemysqlhosting.net",user="sql12593693",password="2nytQApMNx",charset='utf8',database="sql12593693")
    mydb = mysql.connector.connect(host="bsqx344asdfmrehlcqd5-mysql.services.clever-cloud.com",user="ugvj28luz0jwzcjf",password="wvzQGiU131HkHzJ8nhr6",charset='utf8',database="bsqx344asdfmrehlcqd5")
    try:
        loggedin = request.session['loggedin']
    except:
        loggedin = False
    if not loggedin:
        return redirect(home)
    name = request.POST.get("name", "")
    roll = request.POST.get("roll", "")
    message = request.POST.get("message", "")
    msg = ''
    cursor=mydb.cursor()
    if roll != "" and message != "":
        print(name, roll, message)
        cursor.execute('INSERT INTO proposal VALUES(%s, %s, %s, %s, %s)', (request.session["logged_roll"], roll, name, message, ''))
        mydb.commit()
        msg='Proposal Sent Succesfully'
    cursor.execute('SELECT roll, name, branch, batch FROM accounts where roll != %s ORDER BY roll', (request.session["logged_roll"],))
    account = cursor.fetchall()
    cursor.execute('SELECT to_roll FROM proposal where from_roll != %s', (request.session["logged_roll"],))
    proposal = cursor.fetchall()
    for i in proposal:
        for j in account:
            if(i[0]==j[0]):
                account.remove(j)
                break
    cursor.close()
    param = {'account':account, 'msg':msg}
    mydb.close()
    return render(request, 'propose.html', param)

def fillup(request):
    name = request.POST.get("name", "")
    roll = request.POST.get("roll", "")
    email = request.POST.get("email", "")
    year = request.POST.get("year", "")
    branch = request.POST.get("branch", "")
    msg=''
    # mydb = mysql.connector.connect(host="sql12.freemysqlhosting.net",user="sql12593693",password="2nytQApMNx",charset='utf8',database="sql12593693")
    mydb = mysql.connector.connect(host="bsqx344asdfmrehlcqd5-mysql.services.clever-cloud.com",user="ugvj28luz0jwzcjf",password="wvzQGiU131HkHzJ8nhr6",charset='utf8',database="bsqx344asdfmrehlcqd5")
    if name != "" and roll != "" and email != "":
        cursor=mydb.cursor()
        cursor.execute('SELECT * FROM accounts WHERE roll = %s', (roll,))
        account = cursor.fetchone()
        if account:
            msg='account already exists'
        else:
            cursor.execute('INSERT INTO accounts VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (roll, name, email, branch, year, '', '', ''))
            mydb.commit()
            print(name,roll,email, branch, year)
        cursor.close()
    mydb.close()
    param={'msg':msg}
    return render(request, 'fillup.html',param)
