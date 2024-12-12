from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

arya_api = Blueprint('arya_api', __name__, url_prefix='/api')
api = Api(arya_api)

class AryaAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Arya Savlani",
                "age": 15,
                "classes": ["AP Calc", "AP CSP", "AP Chem", "World History", "Offroll"],
                "favorite": {
                    "color": "Red",
                    "number": 8
                }
            })
    

api.add_resource(AryaAPI._A_Person, "/arya")
