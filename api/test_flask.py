import os
import openai
from flask import Flask, Response, request
from datetime import datetime
from flask_cors import CORS
openai.api_key = "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"


app = Flask(__name__)
CORS(app)

@app.route('/stream', methods=['POST'])
def pidato():
    data = request.get_json()
    inputValue = data['inputValue']
    def generate_events():
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=inputValue,
            max_tokens=500,
            temperature=0,
            stream=True,  # this time, we set stream=True
        )

    
        completion_text = ''
        # iterate through the stream of events
        for event in response:
            event_text = event['choices'][0]['text']  # extract the text
            completion_text += event_text  # append the text
            yield event_text  # print the delay and text

        print(f"Full text received: {completion_text}")

    return Response(generate_events(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run()