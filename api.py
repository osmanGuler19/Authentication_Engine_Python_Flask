import flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, jsonify
import Models.crypto as Crypto
from pathlib import Path
from databaseOperations import addUser, getUser, deleteUser, updateUser
import distutils.util as dsUtil
#from Models.usermodel import db

app  = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'iTN4wwiLTOwg_yyGCTEEyLKie9L1uwJviJP7avMDFSE'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///User2.db'
app.static_folder = 'static'


@app.route('/',methods = ['GET'])
def home():
    
    #Site ilk açıldığında buradan başlayacağı için önce key ve preferences dosyası oluşturuldu. Daha önce oluşturulduysa tekrar oluşturulmasına gerek yok
    if Path("sharedPreferences.bin").exists()==False:
        Crypto.createKey()
        Crypto.createSharedPreferencesFile()
        Crypto.addSharedPreferencesData('isFirstOpen','True')
    return "<center><h1>Authentication Engine</h1></center><center><p>This site is a prototype API for authentication engines.</p></center>"


@app.route('/admin')
def admin():
    return render_template('admin_enterance/admin.html')

@app.route('/admin_login', methods = ['POST'])
def admin_login():
    id = request.form['login_id']
    password = request.form['login_password']
    isFirstOpening = dsUtil.strtobool(Crypto.getSharedPreferencesData('isFirstOpen'))
    if(isFirstOpening==True and Path("sharedPreferences.bin").exists()==True and id =='admin' and password =='admin'):
        return render_template('admin_enterance/admin_login.html')

    user = getUser(id, password)
    print(type(addUser('osman-guler@outlook.com','Kumarbaz19.',False,'admin')))

    if(user is not None and ("".join(user[3])).lower()=='admin'.lower()):
        return "<center><h1>Admin Girişi Başarılı</h1></center>"

    if(user is not None):
        return render_template('admin_enterance/deneme.html',value = user[0], value2 = user[3])
    else: return "<center><h1>404</h1><p>The resource could not be found.</p></center>", 404    
        


@app.route('/change_credentials', methods = ['POST'])
def change_credentials():
    #Burada isFirstOpening false yapılacak
    #Crypto.editSharedPreferencesData('isFirstOpen','False')
    new_email= request.form['login_email']
    new_password = request.form['login_password']    
    #addUser(new_email,new_password,True,'admin')
    #Crypto.editSharedPreferencesData('isFirstOpen','False')
    list = getUser(new_email,new_password)
    data = Crypto.getSharedPreferencesAllData()
    return render_template('admin_enterance/deneme.html',value = data, value2 = list[1] ) 

@app.errorhandler(404)
def page_not_found(e):
    return "<center><h1>404</h1><p>The resource could not be found.</p></center>", 404

app.run()

