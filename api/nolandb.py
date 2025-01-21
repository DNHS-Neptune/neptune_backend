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
        
        def get(self):
            nolans = Nolans.query.all()
            return jsonify([nolan.read() for nolan in nolans])
            
        def put(self):
            data = request.get_json()
            if data is None:
                return {'message': 'Post data not found'}, 400
            
            nolan = Nolans.query.get(data['id'])
            if nolan is None:
                return {'message': 'Nolan not found'}, 404
            
            nolan.update({"name": data['name']})
            return jsonify(nolan.read())
        
        def delete(self):
            data = request.get_json()
            if data is None:
                return {'message': 'Post data not found'}, 400
            
            nolan = Nolans.query.get(data['id'])
            if nolan is None:
                return {'message': 'Nolan not found'}, 404
            
            nolan.delete()
            return jsonify({"message": "Nolan deleted"})
                
# Add the route to the API
api.add_resource(NolanDBAPI.User, '/nolandb')
