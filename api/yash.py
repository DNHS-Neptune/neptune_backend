from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

yash_api = Blueprint('yash_api', __name__, url_prefix='/api')
api = Api(yash_api)

class YashAPI:
    class _Y_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Yash Patil",
                "age": 16,
                "classes": ["Advanced Placement Computer Science Principles", "Advance Placement English Seminar 1", "Advance Placement AP Calculus AB", "World History Two"],
                "favorite": {
                    "color": "Green",
                    "number": 21
                }
            })
    

api.add_resource(YashAPI._Y_Person, "/yash")
