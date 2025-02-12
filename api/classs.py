from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app, db
from model.classs import Class
from model.user import User
from api.jwt_authorize import token_required
from flask import Blueprint, request, jsonify, current_app, Response, g

# Create Blueprint and API
class_api = Blueprint('class_api', __name__, url_prefix='/api')
api = Api(class_api)

class ClassAPI:
    class AddClass(Resource):
        @token_required()
        def post(self):
            current_user = g.current_user  # Get the logged-in user

            data = request.get_json()

            try:
                # Validate request data
                if 'pick' not in data:
                    return {"message": "Invalid request. 'pick' is required."}, 400

                user = User.query.filter_by(_uid=current_user.uid).first()  # Fetch user by uid
                if user is None:
                    return {"message": "User not found."}, 404  # Handle the case if user doesn't exist
                
                # Create a new class entry with the logged-in user's ID
                new_class = Class(data['pick'], current_user.name)  # Use user_id instead of 'user'
                new_class.create()

                return new_class.read(), 201
            except Exception as e:
                return {"message": f"Error adding class: {str(e)}"}, 500

            
# READ (GET) - Fetch all classes
        @staticmethod
        def get(self):
            try:
                classes = Class.query.all()
                return [class_item.read() for class_item in classes], 200
            except Exception as e:
                return {"message": f"Error fetching classes: {str(e)}"}, 500

        # UPDATE (PUT)
        @staticmethod
        def put(self):
            data = request.get_json()
            if data is None:
                return {'message': 'Post data not found'}, 400
            
            classss = Class.query.get(data['id'])
            if classss is None:
                return {'message': 'Class not found'}, 404
            
            classss._pick = data["pick"]
            db.session.commit()
            return jsonify(classss.read())
        

        # DELETE (DELETE)
        @staticmethod
        def delete(self):
            try:
                body = request.get_json()
                if not body or 'id' not in body:
                    return {"message": "Invalid request. ID is required."}, 400

                class_to_delete = Class.query.get(body['id'])
                if not class_to_delete:
                    return {"message": "Class not found."}, 404

                db.session.delete(class_to_delete)
                db.session.commit()

                return {"message": "Class deleted successfully."}, 200
            except Exception as e:
                return {"message": f"Error deleting class: {str(e)}"}, 500
# Add the route to the API
api.add_resource(ClassAPI.AddClass, '/class/add')
