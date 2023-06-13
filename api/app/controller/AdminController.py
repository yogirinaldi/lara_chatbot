from app.model.admin import Admin
from app import response, app, db
from flask import request
import datetime

def index():
    try:
        admin = Admin.query.all()
        data = formatArray(admin)
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
        'id_admin': data.id_admin,
        'nama': data.nama,
        'email':data.email
    }

    return data

def detail(id):
    try:
        user = Admin.query.filter_by(id=id).first()
        if not user:
            response.badRequest([],"KOSONG")
        
        data = singleObject(user)
        return response.succeed(data,"success")
    except Exception as e:
        print(e)

def makeAdmin():
    try:
        data = request.get_json()
        nama = data['nama']
        email = data['email']
        password = data['password']

        admin = Admin(nama=nama,email=email)
        admin.setPassword(password)

        db.session.add(admin)
        db.session.commit()
        return response.succeed(True,"BERHASIL MENAMBAH ADMIN")
    except Exception as e:
        print(e)


def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        admin = Admin.query.filter_by(email=email).first()
        if not admin:
            return response.badRequest(False,"Email tidak terdaftar")
        if not admin.checkPassword(password):
            return response.badRequest(False,"Password salah")
        
        data = singleObject(admin)

        
        return response.succeed(data,"BERHASIL LOGIN")
    except Exception as e:
        print(e)