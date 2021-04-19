from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite://///home/cristian/authapi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    email = db.Column(db.String(150))

db.create_all()

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
            data = jwt.decode(token, app.config[SECRET_KEY])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'message': 'Invalid token.'
            })

        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
    data = request.get_json()
    new_user = Users(public_id=str(uuid.uuid4()), email=data['email']) 
    db.session.add(new_user)  
    db.session.commit()    
    return jsonify({
        'message': 'Registered successfully.'
    }), 200

@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    auth = request.authorization   
    if not auth or not auth.email:  
        return make_response('Could not verify', 401, {'WWW.Authentication': 'Basic realm: "Login required"'})    
    user = Users.query.filter_by(email=auth.email).first()   
    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
        return jsonify({'token' : token.decode('UTF-8')}) 

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})