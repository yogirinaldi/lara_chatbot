from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager
from flask_cors import CORS



app = Flask(__name__)
app.secret_key = "lara123"
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app, origins=['http://localhost:3000', 'http://localhost:5000',"http://localhost:3001"], supports_credentials=True)


from app.model import user, question, dataset, admin
from app import routes