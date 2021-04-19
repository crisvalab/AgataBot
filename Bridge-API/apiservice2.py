from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import jwt
import datetime
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/cristian/Desktop/AgataBot-v2/AgataBot/Bridge-API/authapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

API_TRANSLATE_TO_ES = 'http://0.0.0.0:3002/translator/es/'
API_TRANSLATE_TO_EN = 'http://0.0.0.0:3002/translator/en/'
API_OBTAIN_ANSWER = 'http://0.0.0.0:3001/agata/answer/'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    email = db.Column(db.String(150))
    password = db.Column(db.String(50))

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({
                'message': 'A valid token is missing.'
            })
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'message': 'Invalid token.'
            })

        return f(current_user, *args, **kwargs)
    return decorator

def throw_request_error():
    return jsonify({
        'message': 'The intern request not be valid.'
    })

@app.route('/', methods=['GET', 'POST'])
def home_route():
    return jsonify({
        'message': 'Welcome to the Bridge API.',
        'info': 'This API intercommunicates all the rest of the microservices in the network to balance and distribute all the incoming requests.',
        'developer': 'Cristian Valero Abundio'
    })

@app.route('/register/', methods=['POST'])
def signup_user():
    if request.is_json():
        data = request.get_json()  
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = Users(public_id=str(uuid.uuid4()), email=data['email'], password=hashed_password) 
        db.session.add(new_user)  
        db.session.commit()    
        return jsonify({
            'message': 'Registered successfully.'
        }), 200
    return jsonify({
        'message': 'You must send json data only.'
    }), 401

@app.route('/login/', methods=['POST'])  
def login_user(): 
    auth = request.authorization   
    if not auth or not auth.username or not auth.password:  
        return make_response('Could not verify.', 401, {'WWW.Authentication': 'Basic realm: "Login required."'})    
    user = Users.query.filter_by(email=auth.username).first()
    if user != None:
        if check_password_hash(user.password, auth.password):  
            token = jwt.encode({
                'public_id': user.public_id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }, app.config['SECRET_KEY']) 
            return jsonify({'token' : token})
    else:
        return jsonify({
            "message": "Requested user not found."
        })
    return make_response('Could not verify',  401, {'WWW.Authentication': 'Basic realm: "Login required."'})

@app.route('/agata/conversate/en/', methods=['POST'])
@token_required
def generate_english_answer(current_user):
    if request.method == 'POST':
        request_data = request.get_json() #{'id': 3, 'question': ''}
        id, question = str(request_data['id']), str(request_data['question']) 
        req = requests.post(url=API_OBTAIN_ANSWER, json={'id': id, 'question': question})
        if req.status_code == 200:
            answer = req.json()['answer']
            return jsonify({
                'question': str(question),
                'answer': str(answer)
            })
        else:
            throw_request_error()

@app.errorhandler(404)
def route_not_found(exc):
    return jsonify({
        'code': 404,
        'message': 'The route you requested not found. Please, try again or contact with an administrator.'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3005) #when finish, change port to 3000, 3005 is only for testing in production