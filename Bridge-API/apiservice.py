import socket
import requests
from flask import Flask, jsonify, request
from flask_restful import Api

app = Flask(__name__)

API_TRANSLATE = 'http://0.0.0.0:3002/'
API_AGATA = 'http://0.0.0.0:3001/'

API_TRANSLATE_TO_ES = f'{API_TRANSLATE}translator/es/'
API_TRANSLATE_TO_EN = f'{API_TRANSLATE}translator/en/'
API_OBTAIN_ANSWER = f'{API_AGATA}agata/answer/'

def throw_request_error(req):
    return jsonify({
        'message': 'The intern request not be valid.',
        'reason': str(req.reason)
    }), req.status_code

@app.route('/', methods=['GET', 'POST'])
def home_route():
    return jsonify({
        'message': 'Welcome to the Bridge API.',
        'info': 'This API intercommunicates all the rest of the microservices in the network to balance and distribute all the incoming requests.',
        'developer': 'Cristian Valero Abundio'
    }), 200

@app.route('/agata/conversate/en/', methods=['POST'])
def generate_english_answer():
    if request.method == 'POST':
        request_data = request.get_json() #{'id': 3, 'question': ''}
        id, question = str(request_data['id']), str(request_data['question']) 
        req = requests.post(url=API_OBTAIN_ANSWER, data={'id': id, 'question': question})
        if req.status_code == 200:
            answer = req.json()['answer']
            return jsonify({
                'question': str(question),
                'answer': str(answer)
            }), 200
        else:
            throw_request_error(req=req)

@app.route('/agata/conversate/es/', methods=['POST'])
def generate_spanish_answer():
    if request.method == 'POST':
        request_data = request.get_json() #{'id': 3, 'question': ''}
        id, question = str(request_data['id']), str(request_data['question'])
        req = requests.post(url=API_TRANSLATE_TO_EN, data={'sentence': question})
        if req.status_code == 200:
            sentence_to_en = req.json()['translation'] #This is the translated sentence.
            req = requests.post(url=API_OBTAIN_ANSWER, data={'id': id, 'question': sentence_to_en})
            if req.status_code == 200:
                answer = req.json()['answer'] #This is the retrived answer.
                req = requests.post(url=API_TRANSLATE_TO_ES, data={'sentence': answer})
                if req.status_code == 200:
                    sentence_to_es = req.json()['translation']
                    return jsonify({
                        'question': str(question),
                        'question_to_en': str(sentence_to_en),
                        'answer': str(answer),
                        'answer_to_es': str(sentence_to_es)
                    }), 200
                else:
                    throw_request_error(req=req)
            else:
                throw_request_error(req=req)
        else:
            throw_request_error(req=req)

@app.errorhandler(404)
def route_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')