from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app, db
from model.sports import Sports

# Create Blueprint and API
sports_api = Blueprint('sports_api', __name__, url_prefix='/api')
api = Api(sports_api)

class SportsAPI:
    class User(Resource):
        @staticmethod
        def post():
            try:
                # Get request body
                body = request.get_json()
                
                if not body or 'name' not in body:
                    return {"message": "Invalid request. name is required."}, 400
                
                name = body["name"]
                emoji = body["emoji"]

                new_sport = Sports(name=name, emoji=emoji)
                new_sport.create()

                # Return success response
                return new_sport.read(), 201
            except Exception as e:
                return {"message": f"Error adding sport: {str(e)}"}, 500
        
        def get(self):
            sports = Sports.query.all()
            return jsonify([sport.read() for sport in sports])
            
        def put(self):
            data = request.get_json()
            if data is None:
                return {'message': 'Post data not found'}, 400
            
            sport = Sports.query.get(data['id'])
            if sport is None:
                return {'message': 'Sport not found'}, 404
            
            sport.update({"name": data['name']})
            return jsonify(sport.read())
        
        def delete(self):
            data = request.get_json()
            if data is None:
                return {'message': 'Post data not found'}, 400
            
            sport = Sports.query.get(data['id'])
            if sport is None:
                return {'message': 'Sport not found'}, 404
            
            sport.delete()
            return jsonify({"message": "Sport deleted"})
                
# Add the route to the API
api.add_resource(SportsAPI.User, '/sports')