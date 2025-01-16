from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app, db
from model.nolan import Nolans

# Create Blueprint and API
nolandb_api = Blueprint('nolandb_api', __name__, url_prefix='/api')
api = Api(nolandb_api)

class NolanDBAPI:
    class User(Resource):
        @staticmethod
        def post():
            try:
                # Get request body
                body = request.get_json()
                
                if not body or 'name' not in body :
                    return {"message": "Invalid request. name is required."}, 400
                
                name = body["name"]

                new_nolan = Nolans(name=name)
                new_nolan.create()

                # Return success response
                return new_nolan.read(), 201
            except Exception as e:
                return {"message": f"Error adding nolan: {str(e)}"}, 500
        
        def get():
            try:
                nolans = Nolans.query.all()
                return jsonify([nolan.read() for nolan in nolans])
            except Exception as e:
                return {"message": f"Error getting nolans: {str(e)}"}, 500
# Add the route to the API
api.add_resource(NolanDBAPI.User, '/nolandb')
