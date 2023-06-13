from app.model.user import User
from app import response, app, db
from flask import request, session
from datetime import datetime

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
        'id_user': data.id_user,
        'nama': data.nama,
        'email':data.email,
        'usia':data.usia,
        'jk':data.jk,
        'tanggal':data.tanggal.strftime("%Y-%m-%d %H:%M:%S.%f")
    }

    return data

def detail(id):
    try:
        user = User.query.filter_by(id_user=id).first()
        if not user:
            response.badRequest([],"KOSONG")
        
        data = singleObject(user)
        session["userData"] = data
        return response.succeed(data,"success")
    except Exception as e:
        print(e)



def save():
    try:
        data = request.get_json()
        nama = data['nama']
        email = data['email']
        jk = data['jk']
        usia = data['usia']

        user = User(nama=nama,email=email,jk=jk,usia=usia,tanggal=datetime.now())

        db.session.add(user)
        db.session.commit()

        data = singleObject(user)
        session["userData"] = data
        return response.succeed({
            'id_user':user.id_user
            },"BERHASIL MENAMBAH")
    except Exception as e:
        print(e)
