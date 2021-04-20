from router import RouterManager
from flask import Blueprint, request, jsonify
import requests

class AgataRouter(RouterManager):

    def __init__(self, name, app, db, users, api_adress_sources):
        RouterManager.__init__(self, name, app, db, users, api_adress_sources)

    def config_routes(self):
        @self.blueprint.route('/agata/conversate/en/', methods=['POST'])
        @self.token_required
        def generate_english_answer(current_user):
            if request.method == 'POST':
                request_data = request.get_json() #{'id': 3, 'question': ''}
                id, question = str(request_data['id']), str(request_data['question'])
                url = self.api_adress_sources['agata']['answer']
                req = requests.post(url=url, json={'id': id, 'question': question})
                if req.status_code == 200:
                    answer = req.json()['answer']
                    return jsonify({
                        'question': str(question),
                        'answer': str(answer)
                    })
            return jsonify({ 'message': 'Request not valid or internal error. Please contact to the administrator.' })

        @self.blueprint.route('/agata/conversate/es/', methods=['POST'])
        @self.token_required
        def generate_spanish_answer(current_user):
            if request.method == 'POST':
                request_data = request.get_json() #{'id': '3', 'question': 'Hola, ¿como te llamas?'}
                id, question = str(request_data['id']), str(request_data['question'])
                url = self.api_adress_sources['translator']['en']
                req = requests.post(url=url, json={'sentence': question})
                if req.status_code == 200:
                    sentence_to_en = req.json()
                    sentence_to_en = sentence_to_en['translation'] #This is the translated sentence.
                    url = self.api_adress_sources['agata']['answer']
                    req = requests.post(url=url, json={'id': id, 'question': sentence_to_en})
                    if req.status_code == 200:
                        answer = req.json()
                        answer = answer['answer'] #This is the retrived answer.
                        url = self.api_adress_sources['translator']['es']
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

        return self.blueprint