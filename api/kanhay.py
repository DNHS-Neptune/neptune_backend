from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

kanhay_api = Blueprint('kanhay_api', __name__, url_prefix='/api')
api = Api(kanhay_api)

class KanhayAPI:
    class _K_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Kanhay Patil",
                "age": 16,
                "classes": ["Honors Principles of Engineering", "Advanced Placement Computer Science Principles", "Advance Placement English Seminar 1", "Advance Placement AP Calculus AB", "Advance Placement Physics C Mechanics"],
                "favorite": {
                    "color": "Blue",
                    "number": 7
                }
            })
    

api.add_resource(KanhayAPI._K_Person, "/kanhay")
