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

def deleteUser(self, add_email, add_password):
    s = self.users.select().where(self.users.c.email ==add_email)
    resultEmail = self.engine.connect().execute(s)
    query = select(self.users.c.password).where(self.users.c.email == add_email)
    result = self.engine.connect().execute(query)
    id_result = result.first()[0]
    fernet = Fernet(getKey())
    resultToBinary = id_result.encode('UTF-8')
    decryptedPassword = fernet.decrypt(resultToBinary)
    decryptedPasswordToString = decryptedPassword.decode('UTF-8')

    if decryptedPasswordToString.lower() == add_password.lower() and  resultEmail.first() is not None :
        stmt = self.users.update().where(self.users.c.email == add_email).values(isDeleted= True)
        self.engine.connect().execute(stmt)

def updateUser(self,add_email, add_password,add_authenticated,add_role, add_isDeleted,add_isLoggedIn):
    s = self.users.select().where(self.users.c.email ==add_email)
    resultEmail = self.engine.connect().execute(s)
    query = select(self.users.columns.password).where(self.users.c.email == add_email)
    result = self.engine.connect().execute(query)
    id_result = result.first()[0]
    fernet = Fernet(getKey())
    resultToBinary = id_result.encode('UTF-8')
    decryptedPassword = fernet.decrypt(resultToBinary)
    decryptedPasswordToString = decryptedPassword.decode('UTF-8')
    if (decryptedPasswordToString.lower() == add_password.lower() and resultEmail is not None):
        stmt = self.users.update().where(self.users.c.email == add_email).values(email = add_email, password = add_password, authenticated = add_authenticated, role= add_role, isDeleted= add_isDeleted,isLoggedIn = add_isLoggedIn)
        self.engine.connect().execute(stmt)
        return 'Updated'

    else:
        return 'Error'

def getUser(add_email,add_password):
    with engine.connect() as connection:
        s = users.select().where(users.c.email ==add_email) #This is for email
        resultEmail = connection.execute(s)
        u = resultEmail.first()
        query = select(users.c.password).where(users.c.email == add_email)
        result = connection.execute(query)
        if result is not None and u is not None:
            print('Girdi')
            mylist = [r for r in u]
            id_result = result.first()[0]
            fernet = Fernet(getKey())
            resultToBinary = id_result.encode('UTF-8')
            decryptedPassword = fernet.decrypt(resultToBinary)
            decryptedPasswordToString = decryptedPassword.decode('UTF-8')
            if (decryptedPasswordToString.lower() == add_password.lower() and u is not None) :
                return mylist
            else:
                print('İç Else')
                return 'None'
        else:
            print('Dış Else')
            return 'None'
        

def addUser(add_email, add_password,add_authenticated,add_role):
    fernet = Fernet(getKey())
    passwordToBinary = add_password.encode('UTF-8')
    enryptedPassword = fernet.encrypt(passwordToBinary)
    enryptedPasswordToString = enryptedPassword.decode('UTF-8')
    u = getUser(add_email = add_email,add_password = add_password)
    if u is None:
        ins = users.insert().values(email = add_email, password = enryptedPasswordToString, authenticated = add_authenticated, role = add_role.lower() )
        conn = engine.connect()
        conn.execute(ins)
    