from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

akshaj_api = Blueprint('akshaj_api', __name__, url_prefix='/api')
api = Api(akshaj_api)

class AkshajAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "",
                "age": 1,
                "classes": [],
                "favorite": {
                    "color": "",
                    "number": 1
                }
            })
    

api.add_resource(AkshajAPI._A_Person, "/akshaj")
