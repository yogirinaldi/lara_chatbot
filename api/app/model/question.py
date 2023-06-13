from app import db
from app.model.user import User

class Question(db.Model):
    id_question = db.Column(db.BigInteger, primary_key = True, autoincrement=True)
    id_user = db.Column(db.BigInteger, db.ForeignKey(User.id_user))
    pertanyaan = db.Column(db.Text,nullable=False)
    jawaban = db.Column(db.Text,nullable=False)
    feedback = db.Column(db.Boolean,nullable=True)
    tanggal = db.Column(db.DateTime,nullable=False)

    def __repr__(self):
        return '<Question {}>'.format(self.name)