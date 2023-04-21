from app.model.user import User
from app import response, app, db
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime

def index():
    try:
        user = User.query.all()
        data = formatArray(user)
        return response.succeed(data,"success")
    except Exception as e:
        print(e)

def formatArray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))
    
    return array

def singleObject(data):
    data = {
        'id': data.id,
        'name': data.name,
        'email':data.email,
        'level':data.level
    }

    return data

def detail(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            response.badRequest([],"KOSONG")
        
        data = singleObject(user)
        return response.succeed(data,"success")
    except Exception as e:
        print(e)


def makeAdmin():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']
        level = 1

        user = User(name=name,email=email,level=level)
        user.setPassword(password)

        db.session.add(user)
        db.session.commit()
        return response.succeed(True,"BERHASIL MENAMBAH ADMIN")
    except Exception as e:
        print(e)


def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            return response.badRequest(False,"Email tidak terdaftar")
        if not user.checkPassword(password):
            return response.badRequest(False,"Password salah")
        
        data = singleObject(user)
        expires = datetime.timedelta(days=3)
        expires_refresh = datetime.timedelta(days=3)

        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)
        
        return response.succeed({
            'data':data,
            'access_token':access_token,
            'refresh_token':refresh_token
        },"BERHASIL LOGIN")
    except Exception as e:
        print(e)