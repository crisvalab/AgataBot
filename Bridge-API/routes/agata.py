from .router import RouterManager
from flask import Blueprint, request, jsonify
import requests

class AgataRouter(RouterManager):

    def __init__(self, name, app, db, Users, config):
        super().__init__(name, app, db, Users, config)

        services = self.config['SERVICES']
        self.addresses = {
            'translator': {
                'es': f'http://{services["TRANSLATOR-API"]["LISTEN-ADRESS"]}:{services["TRANSLATOR-API"]["PORT"]}/translator/es/',
                'en': f'http://{services["TRANSLATOR-API"]["LISTEN-ADRESS"]}:{services["TRANSLATOR-API"]["PORT"]}/translator/en/'
            },
            'agata': {
                'answer': f'http://{services["GPT2-API"]["LISTEN-ADRESS"]}:{services["GPT2-API"]["PORT"]}/agata/answer/'
            }
        }

    def config_routes(self):
        @self.blueprint.route('/agata/conversate/en/', methods=['POST'])
        @self.token_required
        def generate_english_answer(current_user):
            if request.method == 'POST':
                try:
                    request_data = request.get_json() #{'id': 3, 'question': ''}
                    id, question = str(request_data['id']), str(request_data['question'])
                    url = self.addresses['agata']['answer']
                    req = requests.post(url=url, json={'id': id, 'question': question})
                    if req.status_code == 200:
                        answer = req.json()['answer']
                        return jsonify({
                            'question': str(question),
                            'answer': str(answer)
                        })
                except:
                    return jsonify({'message:': 'Request not valid.'})
            return jsonify({ 'message': 'Request not valid or internal error. Please contact to the administrator.' })

        @self.blueprint.route('/agata/conversate/es/', methods=['POST'])
        @self.token_required
        def generate_spanish_answer(current_user):
            if request.method == 'POST':
                try:
                    request_data = request.get_json() #{'id': '3', 'question': 'Hola, ¿como te llamas?'}
                    id, question = str(request_data['id']), str(request_data['question'])
                    url = self.addresses['translator']['en']
                    req = requests.post(url=url, json={'sentence': question})
                    if req.status_code == 200:
                        sentence_to_en = req.json()
                        sentence_to_en = sentence_to_en['translation'] #This is the translated sentence.
                        url = self.addresses['agata']['answer']
                        req = requests.post(url=url, json={'id': id, 'question': sentence_to_en})
                        if req.status_code == 200:
                            answer = req.json()
                            answer = answer['answer'] #This is the retrived answer.
                            url = self.addresses['translator']['es']
                            req = requests.post(url=url, json={'sentence': answer})
                            if req.status_code == 200:
                                sentence_to_es = req.json()
                                sentence_to_es = sentence_to_es['translation']
                                return jsonify({
                                    'question': str(question),
                                    'question_to_en': str(sentence_to_en),
                                    'answer': str(answer),
                                    'answer_to_es': str(sentence_to_es)
                                }), 200
                            else:
                                return jsonify({ 'message': 'Request not valid or internal error. Please contact to the administrator.' })
                        else:
                            return jsonify({ 'message': 'Request not valid or internal error. Please contact to the administrator.' })
                    else:
                        return jsonify({ 'message': 'Request not valid or internal error. Please contact to the administrator.' })
                except:
                    return jsonify({'message:': 'Request not valid.'})

        return self.blueprint