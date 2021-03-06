import random
import string
from flask import Flask, render_template, request, session, jsonify
from werkzeug.utils import redirect

app=Flask(__name__)
app.secret_key='hjuiikkssp'
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<url>')
def dnamicUrl(url):
    connection = connect(host='localhost', database='student', user='root', password='be2509118')
    cur=connection.cursor()
    query1="select * from urlinfo where encryptedUrl='{}'".format(url)
    cur.execute(query1)
    originalurl=cur.fetchone()
    if originalurl==None:
        return render_template('index.html')
    else:
        print(originalurl[1])
        return redirect(originalurl[1])
@app.route('/urlshortner')
def urlshortner():
    url=request.args.get('link')
    custom=request.args.get('customurl')
    print(custom)
    print("planettech")
    connection = connect(host='localhost', database='student', user='root', password='be2509118')
    cur = connection.cursor()
    encryptedurl=''
    if custom=='':
         while True:
             encryptedurl=createEncryptedUrl()
             query1 = "select * from urlinfo where encryptedUrl='{}'".format(encryptedurl)
             cur.execute(query1)
             xyz=cur.fetchone()
             if xyz==None:
                 break
         print(encryptedurl)
         query="insert into urlinfo(originalUrl,encryptedurl,is_Active)values('{}','{}',1)".format(url,encryptedurl)
         cur=connection.cursor()
         cur.execute(query)
         connection.commit()
         finalencryptedurl='st.in/' + encryptedurl
    else:
        query1 = "select * from urlinfo where encryptedUrl='{}'".format(custom)
        cur.execute(query1)
        xyz = cur.fetchone()
        if xyz == None:
            query = "insert into urlinfo(originalUrl,encryptedUrl,is_Active)values('{}','{}',1)".format(url, custom, 1)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            finalencryptedurl = 'st.in/' + custom
        else:
            return "url already exist"
    return render_template('index.html', finalencryptedUrl=finalencryptedurl, url=url)
def createEncryptedUrl():
    letter = string.ascii_letters + string.digits
    encryptedurl=''
    for i in range(6):
        encryptedurl = encryptedurl + ''.join(random.choice(letter))
    print(encryptedurl)
    return encryptedurl
@app.route('/signup')
def signup():
    return render_template('SignUp.html')

@app.route('/register')
def register():
    email=request.args.get('email')
    username=request.args.get('uname')
    password=request.args.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="be2509118")
    cur = connection.cursor()
    query1 = "select * from userDetails where emailId='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    if xyz==None:
        query = "insert into userDetails(emailId,userName,password,is_Active) values('{}','{}','{}',1)".format(email, username, password)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return 'you are successfully registered'

    else:
        return 'already registered'
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checkLoginIn')
def checkLogIn():
    email=request.args.get('email')
    password=request.args.get('pwd')
    connection = connect(host="localhost", database="student", user="root", password="be2509118")
    cur = connection.cursor()
    query1 = "select * from userdetails where emailId='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz == None:
        return render_template('login.html', xyz='you are not registered')
    else:
        if password==xyz[3]:
            session['email']=email
            session['userid']=xyz[0]
            # return render_template('UserHome.html')
            return redirect('/home')
        else:
            return render_template('login.html', xyz='your password is not correct')

@app.route('/home')
def home():
    if 'userid' in session:
        email=session['email']
        id=session['userid']
        print(id)
        connection = connect(host="localhost", database="student", user="root", password="be2509118")
        cur = connection.cursor()
        query1 = "select * from urlinfo where created_by={}".format(id)
        cur.execute(query1)
        data=cur.fetchall()
        print(data)
        return render_template('UserHome.html',data=data)
    return render_template('login.html')
@app.route('/editUrl',methods=['post'])
def editUrl():
    if 'email' in session:
        email = session['email']
        print(email)
    id=request.form.get('id')
    url=request.form.get('orignalurl')
    encrypted=request.form.get('encrypted')
    return render_template("editUrl.html",url=url,encrypted=encrypted,id=id)

@app.route('/updateUrl',methods=['post'])
def updateUrl():
    id=request.form.get('id')
    url=request.form.get('orignalurl')
    encrypted=request.form.get('encrypted')
    connection = connect(host="localhost", database="student", user="root", password="be2509118")
    cur = connection.cursor()
    query = "select * from urlinfo where encryptedurl='{}'and pk_urlId!={}".format(encrypted, id)
    cur.execute(query)
    data = cur.fetchone()
    if data == None:
       query1="update urlinfo set originalUrl='{}',encryptedUrl='{}' where pk_urlId= {}".format(url,encrypted,id)
       cur.execute(query1)
       connection.commit()
       return redirect('/home')
    else:
        return render_template("editUrl.html", url=url, encrypted=encrypted, id=id, error='short url already exist')

@app.route('/deleteUrl',methods=['post'])
def deleteUrl():
    id = request.form.get('id')
    connection = connect(host="localhost", database="student", user="root", password="be2509118")
    cur = connection.cursor()
    query1 = "delete from urlinfo where pk_urlId="+id
    cur.execute(query1)
    connection.commit()
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('userid',None)
    return render_template('login.html')

@app.route('/apitest',methods=["post"])
def apitest():
    abc=request.get_json()
    print(abc)
    list=[]
    da={}
    connection = connect(host="localhost", database="student", user="root", password="be2509118")
    cur = connection.cursor()
    query = "select * from urlinfo "
    cur.execute(query)
    data=cur.fetchall()
    for i in data:
        da["name"]=i[0]
        da["email"]=i[1]
        list.append(da)
    return jsonify(list)
if __name__=='__main__':
    app.run()