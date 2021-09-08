from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, engine,select
from werkzeug.security import generate_password_hash, check_password_hash
import Models.usermodel as UserModel
from logging.config import dictConfig
from cryptography.fernet import Fernet
import keyring


engine = create_engine('sqlite:///User.db', echo = False)
meta = MetaData()
users = Table(
    'users',meta,
    Column('email',String(40),primary_key=True, nullable=False, unique=True),
    Column('password',String(200), nullable=False,),
    Column('authenticated',Boolean, default=False),
    Column('role',String(20), default='user'),
    Column('isDeleted',Boolean, default=False),
    Column('isLoggedIn',Boolean, default=False)
)

meta.create_all(engine)


def createKey():
    # key generation
    key = Fernet.generate_key()
    keyring.set_password("databaseOperations", "secret_for_database", key.decode('UTF-8'))


def getKey():
    return keyring.get_password("databaseOperations", "secret_for_database")

def initDB():
    createKey()
    meta.create_all(engine)
    print('Created db')

def deleteUser(add_email, add_password):
    s = users.select().where(users.c.email ==add_email)
    res = engine.connect().execute(s)
    u = res.first()
    user = [r for r in u]
    fernet = Fernet(getKey())
    resultToBinary = user[1].encode('UTF-8')
    decryptedPassword = fernet.decrypt(resultToBinary)
    decryptedPasswordToString = decryptedPassword.decode('UTF-8')

    if decryptedPasswordToString == add_password:
        print('Selaaaam')
        stmt = users.update().where(users.c.email == add_email).values(isDeleted=True)
        engine.connect().execute(stmt)

def updateUser(add_email, add_password,add_authenticated,add_role, add_isDeleted,add_isLoggedIn):
    s = users.select().where(users.c.email ==add_email)
    res = engine.connect().execute(s)
    u = res.first()
    user = [r for r in u]
    fernet = Fernet(getKey())
    resultToBinary = user[1].encode('UTF-8')
    decryptedPassword = fernet.decrypt(resultToBinary)
    decryptedPasswordToString = decryptedPassword.decode('UTF-8')
    if (decryptedPasswordToString == add_password and user is not None):
        stmt = users.update().where(users.c.email == add_email).values(email = add_email, password = add_password, authenticated = add_authenticated, role= add_role, isDeleted= add_isDeleted,isLoggedIn = add_isLoggedIn)
        engine.connect().execute(stmt)
        return 'Updated'

    else:
        return 'Error'

def getUser(add_email,add_password):
    with engine.connect() as connection:
        s = users.select().where(users.c.email ==add_email) #This is for email
        res = connection.execute(s)
        u = res.first()
        if u is None:
            return 'None'
        user = [r for r in u]
        if user[1] is not None: 
            fernet = Fernet(getKey())
            resultToBinary = user[1].encode('UTF-8')
            decryptedPassword = fernet.decrypt(resultToBinary)
            decryptedPasswordToString = decryptedPassword.decode('UTF-8')
            if (decryptedPasswordToString == add_password) :
                return user
            else:
                return 'None'
        else:
            return 'None'
        

def addUser(add_email, add_password,add_authenticated,add_role):
    fernet = Fernet(getKey())
    passwordToBinary = add_password.encode('UTF-8')
    enryptedPassword = fernet.encrypt(passwordToBinary)
    enryptedPasswordToString = enryptedPassword.decode('UTF-8')
    u = getUser(add_email,add_password)
    if u =='None':
        ins = users.insert().values(email = add_email, password = enryptedPasswordToString, authenticated = add_authenticated, role = add_role.lower() )
        conn = engine.connect()
        conn.execute(ins)
    
def checkPassword(hashedPassword, normalPassword):
    fernet = Fernet(getKey())
    passwordToBinary = hashedPassword.encode('UTF-8')
    decryptedPassword = fernet.decrypt(passwordToBinary)
    decryptedPasswordToString = decryptedPassword.decode('UTF-8')
    if decryptedPasswordToString == normalPassword:
        return True
    else:
        return False

def decryptPassword(password):
    fernet = Fernet(getKey())
    resultToBinary = password.encode('UTF-8')
    decryptedPassword = fernet.decrypt(resultToBinary)
    decryptedPasswordToString = decryptedPassword.decode('UTF-8')
    return decryptedPasswordToString

def encryptPassword(password):
    fernet = Fernet(getKey())
    passwordToBinary = password.encode('UTF-8')
    enryptedPassword = fernet.encrypt(passwordToBinary)
    enryptedPasswordToString = enryptedPassword.decode('UTF-8')
    return enryptedPasswordToString
