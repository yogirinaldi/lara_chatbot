from app.model.question import Question
from app.model.user import User
from app import response, app, db, embedding_api as ea
from flask import request, jsonify, session, Response
import math
from datetime import datetime

import openai
openai.api_key = "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"

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
        'id_question': data.id_question,
        'id_user':data.id_user,
        'pertanyaan': data.pertanyaan,
        'jawaban':data.jawaban,
        'feedback':data.feedback,
        'tanggal':data.tanggal.strftime("%Y-%m-%d %H:%M:%S.%f")
    }

    return data

def save():
    try:
        data = request.get_json()
        pertanyaan = data['pertanyaan']
        id_user =  data['id_user']
    
        if "userData" not in session:
            user = User.query.filter_by(id_user=id_user).first()
            data = {
                'id_user': id_user,
                'nama': user.nama,
                'email':user.email,
                'usia':user.usia,
                'jk':user.jk
            }
            session["userData"] = data
            

        jawaban = ea.answer_query_with_context(pertanyaan, ea.df, ea.document_embeddings)
        questions = Question(id_user=id_user,pertanyaan=pertanyaan,jawaban=jawaban,tanggal=datetime.now())
          

        db.session.add(questions)
        db.session.commit()
        
        
        return response.succeed({
            'id_question':1,
            'pertanyaan':pertanyaan,
            'jawaban':jawaban
            },"BERHASIL MENAMBAH")
    except Exception as e:
        print(e)
    finally:
        db.session.close()

def detail(id_question):
    try:
        question = Question.query.filter_by(id_question=id_question).first()
        if not question:
            response.badRequest([],"KOSONG")

        data = singleObject(question)
        return response.succeed(data,"success")
    except Exception as e:
        print(e)

def update(id_question):
    try:
        data = request.get_json()
        feedback = data['feedback']

        input = [
            {
            'feedback':feedback
            }
        ]

        question = Question.query.filter_by(id_question=id_question).first()
        question.feedback = feedback

        db.session.commit()
        return response.succeed(input,"BERHASIL UPDATE")
    except Exception as e:
        print(e)
    finally:
        db.session.close()


def stream_question():
    try:
        data = request.get_json()
        pertanyaan = data['inputValue']
        id_user = data['id_user']

        questions = Question(id_user=id_user, pertanyaan=pertanyaan, jawaban="", tanggal=datetime.now())
        db.session.add(questions)
        db.session.flush()
        

        # if "userData" not in session:
        #     user = User.query.filter_by(id_user=1).first()
        #     data = {
        #         'id_user': user.id_user,
        #         'nama': user.nama,
        #         'email':user.email,
        #         'usia':user.usia,
        #         'jk':user.jk
        #         }
        #     session["userData"] = data
                

        #prompt = ea.construct_prompt(inputValue,ea.document_embeddings,ea.df)

        def generate_events():
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=pertanyaan,
                max_tokens=10,
                temperature=0,
                stream=True,  # this time, we set stream=True
            )    
            completion_text = ''
            # iterate through the stream of events
            yield f"{questions.id_question} "
            count_yield = 1
            for event in response:
                event_text = event['choices'][0]['text']  # extract the text
                completion_text += event_text  # append the text
                if count_yield <= 2:
                    count_yield += 1
                else:
                    yield event_text  # print the delay and text

            print(f"Full text received:\n{completion_text}") 
            db.session.commit()

        # return Response(generate_events(), mimetype='text/event-stream')
        return Response(generate_events(), mimetype='text/event-stream')
    except Exception as e:
        print(e)
    finally:
        db.session.close()

def update_jawaban():
    try:
        data = request.get_json()
        id_user = data['id_user']
        pertanyaan = data['pertanyaan']
        jawaban = data['jawaban']

        questions = Question(id_user=id_user, pertanyaan=pertanyaan, jawaban=jawaban, tanggal=datetime.now())
        db.session.add(questions)
        db.session.commit()
        return response.succeed(True,"BERHASIL UPDATE")
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