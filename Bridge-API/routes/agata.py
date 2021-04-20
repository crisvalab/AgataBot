from router import RouterManager
from flask import Blueprint, request, jsonify
import requests

SOURCE_AGATA_API = 'http://0.0.0.0:3001/agata/answer/'

class AgataRouter(RouterManager):

    def __init__(self, name, app, db, users):
        RouterManager.__init__(self, name, app, db, users)

    def config_routes(self):
        blueprint = Blueprint(self.name, __name__)

        @blueprint.route('/agata/conversate/en/', methods=['POST'])
        @self.token_required
        def generate_english_answer(current_user):
            if request.method == 'POST':
                request_data = request.get_json() #{'id': 3, 'question': ''}
                id, question = str(request_data['id']), str(request_data['question']) 
                req = requests.post(url=SOURCE_AGATA_API, json={'id': id, 'question': question})
                if req.status_code == 200:
                    answer = req.json()['answer']
                    return jsonify({
                        'question': str(question),
                        'answer': str(answer)
                    })
            return jsonify({
                'message': 'Request not valid or internal error. Pplease contact to the administrator.'
            })

        return blueprint