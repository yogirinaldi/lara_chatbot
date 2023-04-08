from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import pymysql
import embedding_api as ea


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
@cross_origin(origin="http://localhost:3000")
def handle_post_request():
    data = request.get_json()
    # process the received data
    # ...
    #
    query = data['inputValue']
    answer = ea.answer_query_with_context(query, ea.df, ea.document_embeddings)

    ea.conversation.append({"Q":query,"A":answer})
    #print(ea.conversation)
    response = jsonify({'message': answer})
    #response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')

    return response

if __name__ == '__main__':
    app.run(debug=True)

