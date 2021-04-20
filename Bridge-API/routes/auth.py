from router import RouterManager
from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime

class AuthRouter(RouterManager):

    def __init__(self, name, app, db, users):
        RouterManager.__init__(self, name, app, db, users)

    def config_routes(self):
        blueprint = Blueprint(self.name, __name__)

        @blueprint.route('/register/', methods=['POST'])
        def signup_user():
            data = request.get_json()
            hashed_password = generate_password_hash(data['password'], method='sha256')
            new_user = self.users(public_id=str(uuid.uuid4()), email=data['email'], password=hashed_password) 
            self.db.session.add(new_user)
            self.db.session.commit()
            return jsonify({
                'message': 'Registered successfully.'
            }), 200

        @blueprint.route('/login/', methods=['POST'])  
        def login_user(): 
            auth = request.authorization   
            if not auth or not auth.username or not auth.password:  
                return make_response('Could not verify.', 401, {'WWW.Authentication': 'Basic realm: "Login required."'})    
            user = self.users.query.filter_by(email=auth.username).first()
            if user != None:
                if check_password_hash(user.password, auth.password):  
                    token = jwt.encode({
                        'public_id': user.public_id,
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                        }, self.app.config['SECRET_KEY']) 
                    return jsonify({'token' : token})
            else:
                return jsonify({
                    "message": "Requested user not found."
                })
            return make_response('Could not verify',  401, {'WWW.Authentication': 'Basic realm: "Login required."'})

        return blueprint