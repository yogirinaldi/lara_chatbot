from app import app, response, embedding_api as ea
from app.controller import UserController, QuestionController
from flask import request,jsonify,make_response
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin



@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return response.succeed(current_user,"BERHASIL")

@app.route('/')
def method_name():
    return "tes"


# @app.route('/user', methods=['GET'])
# def get_user():
#     return UserController.index()


# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user_id(user_id):
#     return UserController.detail(user_id)

# @app.route('/user', methods=['POST'])
# def makeAdmin():
#     return UserController.makeAdmin()

@app.route('/login',methods=['POST'])
@cross_origin(origin="http://localhost:3000")
def loginss():
    return UserController.login()

@app.route('/question', methods=['GET','POST'])
def question():
    if request.method == 'GET':
        return QuestionController.index()
    elif request.method == 'POST':
        return QuestionController.save()

@app.route('/question/<int:question_id>', methods=['PUT'])
def question_update(question_id):
    return QuestionController.update(question_id)

@app.route('/question/page', methods=['GET'])
def question_page():
    return QuestionController.paginate()

@app.route('/chat', methods=['POST'])
@cross_origin(origin="http://localhost:3000")
def chat():
    data = request.get_json()
    # process the received data
    # ...
    #
    query = data['inputValue']
    answer = ea.answer_query_with_context(query, ea.df, ea.document_embeddings)

    ea.conversation.append({"Q":query,"A":answer})
    #print(ea.conversation)
    response = make_response(jsonify({'message': answer}))
    #response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')

    return response
