from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

shawn_api = Blueprint('shawn_api', __name__, url_prefix='/api')
api = Api(shawn_api)

class ShawnAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Shawn Ray",
                "age": 15,
                "classes": ["AP Calculus AB", "AP CSP", "AP Chemistry", "World History", "Photography"],
                "favorite": {
                    "color": "Blue",
                    "number": 1
                }
            })
    

api.add_resource(ShawnAPI._A_Person, "/shawn")