from flask import Blueprint, jsonify, request
from functools import wraps
import jwt

class RouterManager():

    def __init__(self, name, app, db, Users, config):
        self.name = name
        self.app = app
        self.db = db
        self.Users = Users
        self.config = config
        self.blueprint = Blueprint(self.name, __name__)

    def config_routes(self) -> Blueprint:
        pass

    ''' This function controll accesing routes from external IP adress.
        External requests -> JWT AUTH -> GRANT ACCESS
        Internal requests / Local requests -> GRANT ACCESS DIRECTLY '''
    def token_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if request.remote_addr != 'REPLACE WITH 127.0.0.1':
                if 'x-access-tokens' in request.headers:
                    token = request.headers['x-access-tokens']
                    data = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
                    current_user = self.Users.query.filter_by(public_id=data['public_id']).first()
                    return f(current_user, *args, **kwargs)
                    # try:
                    #     data = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
                    #     current_user = self.Users.query.filter_by(public_id=data['public_id']).first()
                    #     return f(current_user, *args, **kwargs)
                    # except:
                    #     return jsonify({ 'message': 'Invalid token.' })
                else:
                    return jsonify({ 'message': 'A valid token is missing.' })
            else:
                return f(None, *args, **kwargs)
        return decorator