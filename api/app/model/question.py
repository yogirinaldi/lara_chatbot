from app import db
from datetime import datetime

import pytz

# set the timezone to Jakarta
jakarta_timezone = pytz.timezone('Asia/Jakarta')

class Question(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement=True)
    question = db.Column(db.Text,nullable=False)
    answer = db.Column(db.Text,nullable=False)
    feedback = db.Column(db.Boolean,nullable=True)
    date = db.Column(db.DateTime,default=datetime.now(jakarta_timezone))

    def __repr__(self):
        return '<Question {}>'.format(self.name)