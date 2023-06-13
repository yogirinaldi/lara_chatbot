from app import app, response, embedding_api as ea
from app.controller import AdminController, QuestionController,UserController, DatasetController
from flask import request,jsonify,make_response, session
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin



# @app.route('/protected', methods=['GET'])
# @jwt_required
# def protected():
#     current_user = get_jwt_identity()
#     return response.succeed(current_user,"BERHASIL")



@app.route('/')
def method_name():
    session["kucing"] = "anjing"
    return str(session["userData"]) + str(session["kucing"])

@app.route('/makeAdmin', methods=['POST'])
def makeAdmin():
    return AdminController.makeAdmin()

@app.route('/login',methods=['POST'])
def loginss():
    return AdminController.login()

@app.route('/question', methods=['GET','POST'])
def question():
    if request.method == 'GET':
        return QuestionController.index()
    elif request.method == 'POST':
        return QuestionController.save()

@app.route('/question/<int:id_question>', methods=['PUT','GET'])
def questionbyid(id_question): 
    if request.method == 'GET':
        return QuestionController.detail(id_question)
    elif request.method == 'PUT':
        return QuestionController.update(id_question)


@app.route('/streamQuestion', methods=['POST'])
def stream_question():
    return QuestionController.stream_question()


# @app.route('/question/page', methods=['GET'])
# def question_page():
#     return QuestionController.paginate()

# @app.route('/chat', methods=['POST'])
# @cross_origin(origin="http://localhost:3000")
# def chat():
#     data = request.get_json()
#     # process the received data
#     # ...
#     #
#     query = data['inputValue']
#     answer = ea.answer_query_with_context(query, ea.df, ea.document_embeddings)

#     ea.conversation.append({"Q":query,"A":answer})
#     #print(ea.conversation)
#     response = make_response(jsonify({'message': answer}))
#     #response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')

#     return response

@app.route('/user',methods=['POST','GET'])
def user():
    if request.method == 'GET':
        return UserController.index()
    elif request.method == 'POST':
        return UserController.save()
    
@app.route('/user/<int:id_user>',methods=['GET'])
def userbyid(id_user):
    return UserController.detail(id_user)

@app.route('/dataset',methods=['POST','GET',"DELETE"])
def dataset():
    if request.method == 'GET':
        return DatasetController.index()
    elif request.method == 'POST':
        return DatasetController.save()
    elif request.method == 'DELETE':
        return DatasetController.delete()
    
@app.route('/dataset/<int:id_data>',methods=['PUT'])
def datasetbyid(id_data):
    return DatasetController.update(id_data)

@app.route('/cek',methods=['GET'])
def cek():
    return DatasetController.cek()