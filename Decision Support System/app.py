from pickle import TRUE
import pandas as pd
import plotly.figure_factory as ff
import json
import plotly
import plotly.express as px
import plotly.graph_objects as px
import matplotlib.pyplot as plt
from flask import Flask,url_for,redirect,render_template,session
from flask import request
import pickle
import re
import numpy as np
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '08420'
app.config['MYSQL_DB'] = 'dssms'
 
 
mysql = MySQL(app)
model=pickle.load(open('model.pkl','rb'))

@app.route("/",methods=['GET','POST'])
def hello_world():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM uaccount WHERE uname = % s AND upassword = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['uid']
            session['username'] = account['uname']
            user=session['username']
            msg = 'Logged in successfully'
            session['admin']='login'
            vis='none'
            session['vis']=vis
            return redirect(url_for('home', user = user))
            #return render_template('mindstate.html', message = msg,visibility="hidden",**locals())
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html',message=msg,**locals())
@app.route('/predict',methods=['POST'])
def predict():
    a=session.get('admin')
    vis=''
    if a=='admin':
        vis="block"
    elif a=='login':
        vis="none"
    decision=''
    col=''
    li=[request.form["Age"],request.form["LowAlpha"],request.form["HighAlpha"],request.form["LowBeta"],request.form["HighBeta"],request.form["LowGamma"],request.form["HighGamma"]]
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)
    x=''.join(prediction)
    if x=='Neutral':
        decision='The patient is in normal emotional state. All the frequencies are in normal range.\nNo abnormal frequencies were detected from frontal,parietal and occipital lobe.'
        col='black'
    elif x=='Positive':
        decision='The patient is in normal emotional state. Patient may be Happy,Excited or Mentally Calm.\n No abnormalities were found from the frequncies.'
        col='green'
    elif x=='Depressed':
        decision='The Patient is Depressed.It is possible to have Headache,Vomiting.\nPossibily Pseudobulbar affect can be seen for log term depression.Sertraline hydrochloride related medicine can be a cure for this state.'
        col='red'
    else:
        decision='The patient is in Anxiety.Possible Symptoms can be - Tensed, Nervous, Hyperventilation.\n Longterm anxiety can cause Trouble concentrating or thinking,sudden panic,chronic pain,digestive bowel problem and many more.'     
        col='orange'
    u=session.get("username")
    freq=['Low Alpha','High Alpha','Low Beta','High Beta','Low Gamma','High Gamma']
    obtained=[li[1],li[2],li[3],li[4],li[5],li[6]]
    normal=[8,12,13,30,30,60]
    fig = px.Figure(data=[px.Bar(
    name = 'Normal',
    x = freq,
    y = normal
    ),
                       px.Bar(
    name = 'Obtained',
    x = freq,
    y = obtained
   )
   ] )
    fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('mindstate.html',user=u,grapJSON=graphJSON,visibility=vis,color=col,age=li[0],lowalpha=li[1],highalpha=li[2],lowbeta=li[3],highbeta=li[4],lowgamma=li[5],highgamma=li[6],pred=''.join(prediction),des=decision,**locals())
#,name=li[0],gender=li[2],age=li[1],lowalpha=li[3],highalpha=li[4],lowbeta=li[5],highbeta=li[6],lowgamma=li[7],highgamma=li[8],


@app.route('/report',methods=['GET','POST'])
def report():
    
    if request.method=="POST" and 'name' in request.form and 'gen' in request.form and 'age' in request.form and 'la' in request.form and 'ha' in request.form and 'lb' in request.form and 'hb' in request.form and 'lg' in request.form and 'hg' in request.form and 'ms' in request.form and 'rf' in request.form:
        if request.form["name"]=='' or request.form["gen"]=='' or request.form["age"]=='' or request.form["la"]=='' or request.form["ha"]=='' or request.form["lb"]=='' or request.form["hb"]=='' or request.form["lg"]=='' or request.form["hg"]=='' or request.form["ms"]=='' or request.form["rf"]=='':
            m='Input Cannot be Empty'
            return render_template('Report.html',info=m,visibility="hidden",**locals())
        else:
            pinfo=[request.form["name"],request.form["gen"],request.form["age"],request.form["la"],request.form["ha"],request.form["lb"],request.form["hb"],request.form["lg"],request.form["hg"],request.form["ms"],request.form["rf"],request.form["cmt"]]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO patientinfo VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (pinfo[0], pinfo[1], pinfo[2], pinfo[3], pinfo[4], pinfo[5], pinfo[6], pinfo[7], pinfo[8],pinfo[9],pinfo[10], ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('Report.html',n=pinfo[0],ge=pinfo[1],a=pinfo[2],la=pinfo[3],ha=pinfo[4],lb=pinfo[5],hb=pinfo[6],lg=pinfo[7],hg=pinfo[8],ms=pinfo[9],rf=pinfo[10],cmt=pinfo[11],mesg=msg,visibility="visible",**locals())
    return render_template('Report.html',visibility="hidden",**locals())#,a=age,la=lowalpha,ha=highalpha,lb=lowbeta,hb=highbeta,lg=lowgamma,hg=highgamma,s=state)


@app.route('/register',methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM uaccount WHERE uname = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO uaccount VALUES (NULL, % s, % s, % s)', (username,email,password,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html',message=msg,**locals())
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect('/')

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    session['admin']='admin'
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adminaccount WHERE aname = % s AND apassword = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['aid']
            session['username'] = account['aname']
            user=session['username']
            msg = 'Logged in successfully !'
            vis='block'
            session['vis']=vis
            return redirect(url_for('home', user = user+"(Admin)"))
            #return render_template('mindstate.html', mess = msg,visibility="visible",**locals())
        else:
            msg = 'Incorrect username / password !'
    return render_template('Admin.html',mess=msg,**locals())

@app.route('/patientdata')
def patientdata():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from patientinfo")
    data=cursor.fetchall()
    return render_template('patientdata.html',info=data,**locals())
@app.route('/home')
def home():
    visi=session.get('vis')
    u=session.get("username")

    return render_template('mindstate.html',visibility=visi,user=u,see="none",**locals())
@app.route('/manageuser',methods=['GET','POST'])
def manageuser():
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM uaccount")
    data=cur.fetchall()
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM uaccount WHERE uname = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            return redirect(url_for('manageuser'))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
            return redirect(url_for('manageuser'))
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
            return redirect(url_for('manageuser'))
        else:
            cursor.execute('INSERT INTO uaccount VALUES (NULL, % s, % s, % s)', (username,email,password,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('manageuser'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return redirect(url_for('manageuser'))
    return render_template('Manageuser.html',dt=data,m=msg,**locals())

@app.route('/delete/<int:id>', methods = ['GET','POST','DELETE'])
def delete(id):
   id=int(id)
   cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   cur.execute("DELETE FROM uaccount WHERE uid= %s", (id,))
   mysql.connection.commit()
   return redirect(url_for('manageuser'))
'''@app.route('/prescribe',methods=['GET','POST'])
def prescribe():
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        gen=request.form["gen"]
        phn=request.form["phone"]
        cv=request.form["cdate"]
        nv=request.form["ndate"]
        state=request.form["state"]
        tests=request.form.getlist("test")
        med=request.form.getlist("med")
        dname=session.get("username")
        cur1=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur1.execute("select * from uaccount where uname= %s ",(dname,))
        dinfo=cur1.fetchall()
        did=dinfo[0]["uid"]
        cur2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur2.execute('INSERT INTO prescription VALUES ( % s,NULL,% s, % s, % s, % s, % s, % s, % s)',(did,name,phn,age,gen,cv,nv,state,))
        mysql.connection.commit()
        for i in range(len(tests)):
             cur2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             cur2.execute('INSERT INTO test VALUES ( % s,% s, % s, % s)',(did,phn,name,tests[i],))
             mysql.connection.commit()
        for j in range(len(med)):
             cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             cur3.execute('INSERT INTO medicine VALUES ( % s,% s, % s, % s)',(did,phn,name,med[j],))
             mysql.connection.commit()
        redirect(url_for("prescribe"))
         
    return render_template('Prescribe.html',**locals())'''

if __name__=='__main__':
    app.run(debug=TRUE,port=4000)