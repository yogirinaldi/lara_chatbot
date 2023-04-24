from app import db
from datetime import datetime, date

import pytz

# set the timezone to Jakarta
jakarta_timezone = pytz.timezone('Asia/Jakarta')

class Location(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement=True)
    ip_address = db.Column(db.String(15), index=True, nullable=False)
    city = db.Column(db.String(50),nullable=False)
    region = db.Column(db.String(50),nullable=False)
    isp = db.Column(db.String(100),nullable=False)
    date = db.Column(db.DateTime,default=datetime.now(jakarta_timezone))

    def __repr__(self):
        return '<Location {}>'.format(self.name)