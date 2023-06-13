from app import db

class Dataset(db.Model):
    id_data = db.Column(db.BigInteger, primary_key = True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    heading = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)

    def __repr__(self):
        return '<Dataset {}>'.format(self.name)
    
