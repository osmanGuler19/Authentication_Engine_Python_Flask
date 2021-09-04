import flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, jsonify
import Models.crypto as Crypto
from pathlib import Path
from databaseOperations import addUser, getUser, deleteUser, updateUser
import distutils.util as dsUtil
import jwt
import datetime
from functools import wraps
#from Models.usermodel import db

app  = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'iTN4wwiLTOwg_yyGCTEEyLKie9L1uwJviJP7avMDFSE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.static_folder = 'static'

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None
    
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config[SECRET_KEY])
            current_user = getUser(data['email'],data['password'])
        except:
            return jsonify({'message': 'token is invalid'})
         
    
        return f(current_user, *args, **kwargs)
   return decorator



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
    ##addUser('osman-guler@outlook.com','Kumarbaz19.',False,'admin')

    if(user != 'None' and ("".join(user[3])).lower()=='admin'.lower()): #user[3] is role field
        return "<center><h1>Admin Girişi Başarılı</h1></center>"

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
    return render_template('admin_enterance/deneme.html',value = data, value2 = list[1]) 

@app.errorhandler(404)
def page_not_found(e):
    return "<center><h1>404</h1><p>The resource could not be found.</p></center>", 404




app.run(ssl_context=('cert.pem', 'key.pem'), port=443)

'''
'''