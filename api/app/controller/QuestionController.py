from app.model.question import Question
from app import response, app, db, embedding_api as ea
from flask import request, jsonify
import math

def index():
    try:
        question = Question.query.all()
        if not question:
            return response.badRequest([],"KOSONG")
        else:
            data = formatArray(question)        
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
        'question': data.question,
        'answer':data.answer,
        'feedback':data.feedback,
        'date':data.date
    }

    return data

def save():
    try:
        data = request.get_json()
        question = data['question']
        ip_address = data['ip_address']

        answer = ea.answer_query_with_context(question, ea.df, ea.document_embeddings)
        questions = Question(question=question,answer=answer,ip_address=ip_address)

        ea.conversation.append({"Q":question,"A":answer})

        db.session.add(questions)
        db.session.commit()
        return response.succeed({
            'id':questions.id,
            'question':question,
            'answer':answer
            },"BERHASIL MENAMBAH")
    except Exception as e:
        print(e)

def update(question_id):
    try:
        data = request.get_json()
        feedback = data['feedback']

        input = [
            {
            'feedback':feedback
            }
        ]

        question = Question.query.filter_by(id=question_id).first()
        question.feedback = feedback

        db.session.commit()
        return response.succeed(input,"BERHASIL UPDATE")
    except Exception as e:
        print(e)


#pagination
def get_pagination(clss, url, start, limit):
    result = clss.query.all()
    data = formatArray(result)
    count = len(data)

    obj= {}

    if count < start:
        obj['success'] = False
        obj['message'] = "page yang terpilih melebihi batas total data"
        return obj
    else:
        obj['success'] = True
        obj['start_page'] = start
        obj['per_page'] = limit
        obj['total_data'] = count
        obj['total_page'] = math.ceil(count/limit)

        #previous link
        if start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, start - limit)
            limit_copy = start - 1
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)

        #next link
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)

        obj['result'] = data[(start-1):(start-1+limit)]
        return obj
    
def paginate():
    start = request.args.get('start')
    limit = request.args.get('limit')

    try:
        if start == None or limit == None:
            return jsonify(get_pagination(
                Question,
                'http://127.0.0.1:5000/question/page',
                start=request.args.get('start',1),
                limit=request.args.get('limit',3)
                ))
        else:
            return jsonify(get_pagination(
                Question,
                'http://127.0.0.1:5000/question/page',
                start=int(start),
                limit=int(limit)
                ))
    except Exception as e:
        print(e)