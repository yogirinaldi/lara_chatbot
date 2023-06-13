# from app.model.location import Location
# from app import response, app, db
# from flask import request
# from datetime import datetime

# import pytz

# # set the timezone to Jakarta
# jakarta_timezone = pytz.timezone('Asia/Jakarta')

# def index():
#     try:
#         location = Location.query.all()
#         if not location:
#             return response.badRequest([],"KOSONG")
#         else:
#             data = formatArray(location)        
#             return response.succeed(data,"success")
#     except Exception as e:
#         print(e)

# def formatArray(datas):
#     array = []

#     for i in datas:
#         array.append(singleObject(i))
    
#     return array

# def singleObject(data):
#     data = {
#         'id': data.id,
#         'ip_adrress': data.ip_adrress,
#         'city':data.city,
#         'region':data.region,
#         'isp':data.isp,
#         'date':data.date
#     }

#     return data

# def save():
#     try:
#         data = request.get_json()
#         ip_address = data['ip_address']
#         city = data['city']
#         region=data['region']
#         isp=data['isp']        
        
#         location_ip = Location.query.filter_by(ip_address=ip_address).first()

#         if location_ip:
#             if location_ip.date.date() != datetime.now(jakarta_timezone).date():
#                 location = Location(ip_address=ip_address,city=city,region=region,isp=isp)            
#                 db.session.add(location)
#                 db.session.commit()
#                 return response.succeed({
#                     'id':location.id,
#                     'ip_address':location.ip_address,
#                     'city':location.city,
#                     'date':location.date
#                 },"BERHASIL MENAMBAH")  
                          
#             else:
#                 return response.badRequest(False,"Sudah terdaftar")
            
#         else:
#             location = Location(ip_address=ip_address,city=city,region=region,isp=isp)            
#             db.session.add(location)
#             db.session.commit()
#             return response.succeed({
#                 'id':location.id,
#                 'ip_address':location.ip_address,
#                 'city':location.city,
#                 'date':location.date
#             },"BERHASIL MENAMBAH")
                
#     except Exception as e:
#         print(e)