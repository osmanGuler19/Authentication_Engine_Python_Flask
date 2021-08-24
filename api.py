import flask
from flask import render_template, request, jsonify
import Models.crypto as Crypto
from pathlib import Path

app  = flask.Flask(__name__)
app.config["DEBUG"] = True
app.static_folder = 'static'

@app.route('/',methods = ['GET'])

def home():
    #Site ilk açıldığında buradan başlayacağı için önce key ve preferences dosyası oluşturuldu. Daha önce oluşturulduysa 
    if Path("sharedPreferences.bin").exists()==False:
        Crypto.createKey()
        Crypto.createSharedPreferencesFile()
    #First_Open.editSharedPreferencesData('False')
    return "<center><h1>Authentication Engine</h1></center><center><p>This site is a prototype API for authentication engines.</p></center>"


@app.route('/admin')
def admin():
    return render_template('admin_enterance/admin.html')

@app.route('/admin_login', methods = ['POST'])
def admin_login():
    id = request.form['login_id']
    password = request.form['login_password']
    isFirstOpening = bool(Crypto.getSharedPreferencesData)

    if(isFirstOpening==True and Path("sharedPreferences.bin").exists()==True):
        
        return render_template('admin_enterance/admin_login.html', value = Crypto.getSharedPreferencesData("isFirstOpen"))
    
    return "<center><h1>FORM</h1><p>Burası form kısmı</p></center>"


@app.errorhandler(404)
def page_not_found(e):
    return "<center><h1>404</h1><p>The resource could not be found.</p></center>", 404





app.run()


'''@app.route('/admin_login', methods = ['POST'])
def admin_login():
    id = request.form['login_id']
    password = request.form['login_password']
    isFirstOpening = bool(First_Open.getSharedPreferencesData)

    if(isFirstOpening):
        
        return render_template('admin_enterance/admin_login.html', value = First_Open.getSharedPreferencesData())
    
    return "<center><h1>FORM</h1><p>Burası form kısmı</p></center>"
'''

'''
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

'''