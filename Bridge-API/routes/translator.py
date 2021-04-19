from flask import Blueprint, request, jsonify
from apiservice2 import token_required, throw_request_error

translator = Blueprint('translator', __name__)