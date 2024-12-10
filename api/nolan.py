from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

nolan_api = Blueprint('nolan_api', __name__, url_prefix='/api')
api = Api(nolan_api)

class NolanAPI:
    class _N_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Nolan Hightower",
                "age": 15,
                "classes": ["Int 3A", "AP CSP", "AP Sem", "Spanish 5", "AP World"],
                "favorite": {
                    "color": "red",
                    "number": 32
                }
            })
    

api.add_resource(NolanAPI._N_Person, "/nolan")
