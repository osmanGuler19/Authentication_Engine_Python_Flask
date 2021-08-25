from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, update, insert
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'user'

    email = db.Column(db.String, primary_key = True, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    authenticated = db.Column(db.Boolean, default = False)
    role = db.Column(db.String, default = 'user')
    isDeleted = db.Column(db.Boolean, default = False)
    isItLoggedIn = db.Column(db.Boolean,default = False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


def addUser(add_email, add_password,add_authenticated,add_role,table_name):
    insert(table_name).values(email = add_email, password = add_password, authenticated = add_authenticated, role = add_role )


def updateUser(user_email,user_password,user_authentication,user_role,table_name):
    update(table_name).where(email= user_email)