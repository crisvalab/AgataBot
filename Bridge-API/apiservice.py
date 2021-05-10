import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from routes.agata import AgataRouter
from routes.auth import AuthRouter

config = {}
with open('config.json') as config_file:
    config = json.loads(config_file.read())

db_config = config['MySQL']
MYSQL_URI = f'mysql+pymysql://{db_config["USER"]}:{db_config["PASSWORD"]}@{db_config["HOST"]}:{db_config["PORT"]}/{db_config["DATABASE"]}'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = config['JWT-SECRET']
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URI
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3600
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    email = db.Column(db.String(150))
    password = db.Column(db.String(50))

routers = [
    AuthRouter('AuthRouter', app, db, Users, config),
    AgataRouter('AgataRouter', app, db, Users, config)
]

@app.route('/', methods=['GET', 'POST'])
def home_route():
    return jsonify({
        'message': 'Welcome to the Bridge API.',
        'info': 'This API intercommunicates all the rest of the microservices in the network to balance and distribute all the incoming requests.',
        'developer': 'Cristian Valero Abundio'
    }), 200

@app.errorhandler(404)
def route_not_found(exc):
    return jsonify({
        'code': 404,
        'message': 'The route you requested not found. Please, try again or contact with an administrator.'
    }), 404

if __name__ == '__main__':
    db.create_all()
    for router in routers:
         app.register_blueprint(router.config_routes())
    app.run(host='0.0.0.0', port=3000)