from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'user'

    email = db.Column(db.String, primary_key = True, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    authenticated = db.Column(db.Boolean, default = False)
    role = db.Column(db.String, default = 'user')

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
