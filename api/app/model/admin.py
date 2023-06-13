from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model):
    id_admin = db.Column(db.BigInteger, primary_key = True, autoincrement=True)
    nama = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=False, index=True)
    password = db.Column(db.String(102),nullable=False)

    def __repr__(self):
        return '<Admin {}>'.format(self.name)
    
    def setPassword(self,password):
        self.password = generate_password_hash(password)

    def checkPassword(self,password):
        return check_password_hash(self.password,password)