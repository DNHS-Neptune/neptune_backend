from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app, db
from model.nolan import Nolans

# Create Blueprint and API
nolandb_api = Blueprint('nolandb_api', __name__, url_prefix='/api')
api = Api(nolandb_api)

class NolanDBAPI:
    class User(Resource):
        def post(self):
            try:
                # Get request body
                body = request.get_json()
                
                if not body:
                    return {"message": "Invalid request."}, 400
                
                if 'front' not in body:
                    return {"message": "Front of card not found."}, 400
                
                if 'back' not in body:
                    return {"message": "Back of card not found."}, 400
                
                front = body['front']
                back = body['back']

                new_nolan = Nolans(front=front, back=back)
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
            
            nolan.update({'front': data['front'], 'back': data['back']})
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
api.add_resource(NolanDBAPI.User, '/flashcards')
