from app import db

class User(db.Model):
    id_user = db.Column(db.BigInteger, primary_key = True, autoincrement=True)
    nama = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),index=True,nullable=False)
    usia = db.Column(db.Integer,nullable=False)
    jk = db.Column(db.String(10),nullable=False)
    tanggal = db.Column(db.DateTime,nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)
    
