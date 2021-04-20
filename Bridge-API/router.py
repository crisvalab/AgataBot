from flask import Blueprint, jsonify, request
from functools import wraps
import jwt

class RouterManager():

    def __init__(self, name, app, db, users):
        self.name = name
        self.app = app
        self.db = db
        self.users = users

    def config_routes(self) -> Blueprint:
        pass

    def token_required(self, f):
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
                data = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = self.users.query.filter_by(public_id=data['public_id']).first()
            except:
                return jsonify({
                    'message': 'Invalid token.'
                })

            return f(current_user, *args, **kwargs)
        return decorator