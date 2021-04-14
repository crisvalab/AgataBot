from flask import Flask, jsonify, request, json
from flask_restful import Api
from translator import Translator

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def home_route():
    return jsonify({
        'message': 'Welcome to Translator EN-ES/ES-EN API.',
        'info': 'This API only will run from 0.0.0.0 and is for local use only.',
        'developer': 'Cristian Valero Abundio'
    })

@app.route('/translator/es/', methods=['POST'])
def translate_to_es():
    if request.method == 'POST':
        request_data = request.get_json() #{'sentence': 'Hy! My name is Cristian.'}
        sentence = str(request_data['sentence'])
        translation = translator.translate_to_spanish(sentence)
        return jsonify({
            'sentence': sentence,
            'translation': str(translation)
        })

@app.route('/translator/en/', methods=['POST'])
def translate_to_en():
    if request.method == 'POST':
        request_data = request.get_json() #{'sentence': 'Hola, me llamo Paco.'}
        sentence = str(request_data['sentence'])
        translation = translator.translate_to_english(sentence)
        return jsonify({
            'sentence': sentence,
            'translation': translation
        })

@app.errorhandler(404)
def route_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(port=3002, host='0.0.0.0')