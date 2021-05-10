from .router import RouterManager
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime

class AuthRouter(RouterManager):

    def __init__(self, name, app, db, Users, config):
        super().__init__(name, app, db, Users, config)

    def config_routes(self):
        @self.blueprint.route('/register/', methods=['POST'])
        def signup_user():
            data = request.get_json()
            user = self.Users.query.filter_by(email=data['email']).first()
            if user == None:
                hashed_password = generate_password_hash(data['password'], method='sha256')
                new_user = self.Users(public_id=str(uuid.uuid4()), email=data['email'], password=hashed_password) 
                self.db.session.add(new_user)
                self.db.session.commit()
                return jsonify({ 'message': 'Registered successfully.' }), 200
            return jsonify({ 'message': 'User already exists. Please, try again with a diferent email.' }), 401

        @self.blueprint.route('/login/', methods=['POST'])  
        def login_user(): 
            auth = request.authorization   
            if not auth or not auth.username or not auth.password:  
                return make_response('Could not verify.', 401, {'WWW.Authentication': 'Basic realm: "Login required."'})    
            user = self.Users.query.filter_by(email=auth.username).first()
            if user != None:
                if check_password_hash(user.password, auth.password):  
                    token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, self.app.config['SECRET_KEY']) 
                    return jsonify({'token' : token})
                else:
                    return jsonify({ "message": "Invalid email or password." })
            else:
                return jsonify({ "message": "Requested user not found." })
            return make_response('Could not verify',  401, {'WWW.Authentication': 'Basic realm: "Login required."'})

        return self.blueprint