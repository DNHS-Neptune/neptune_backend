from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app, db
from model.classs import Class

# Create Blueprint and API
sports_api = Blueprint('sports_api', __name__, url_prefix='/api')
api = Api(sports_api)

class SportAPI:
    class AddSport(Resource):
        @staticmethod
        def post():
            try:
                # Get request body
                body = request.get_json()
                
                if not body or 'sport' not in body or 'emoji' not in body:
                    return {"message": "Invalid request. all 3 categories  are required."}, 400
                
                sport = body['sport']
                emoji = body['emoji']


                # Create a new period
                new_sport = Class(sport=sport, emoji=emoji)
                new_sport.create()

                # Return success response
                return new_sport.read(), 201
            except Exception as e:
                return {"message": f"Error adding class: {str(e)}"}, 500
            
# READ (GET) - Fetch all classes
        @staticmethod
        def get():
            try:
                sports = Class.query.all()
                return [sport_item.read() for sport_item in sports], 200
            except Exception as e:
                return {"message": f"Error fetching sports: {str(e)}"}, 500

        # UPDATE (PUT)
        @staticmethod
        def put():
            data = request.get_json()
            if data is None:
                return {'message': 'Post data not found'}, 400
            
            sports = Class.query.get(data['id'])
            if sports is None:
                return {'message': 'sport not found'}, 404
            
            sports._pick = data["pick"]
            db.session.commit()
            return jsonify(sports.read())
        

        # DELETE (DELETE)
        @staticmethod
        def delete():
            try:
                body = request.get_json()
                if not body or 'id' not in body:
                    return {"message": "Invalid request. ID is required."}, 400

                sport_to_delete = Class.query.get(body['id'])
                if not sport_to_delete:
                    return {"message": "sport not found."}, 404

                db.session.delete(sport_to_delete)
                db.session.commit()

                return {"message": "Sport deleted successfully."}, 200
            except Exception as e:
                return {"message": f"Error deleting sport: {str(e)}"}, 500
# Add the route to the API
api.add_resource(SportAPI.AddSport, '/sport')
