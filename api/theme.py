import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.themes import Theme

theme_api = Blueprint('theme_api', __name__, url_prefix='/api')

api = Api(theme_api)

class ThemeAPI:
    class _CRUD(Resource):
        def get(self): 
            return jsonify(Theme.query.all())