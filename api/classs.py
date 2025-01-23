from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app, db
from model.classs import Class

# Create Blueprint and API
class_api = Blueprint('class_api', __name__, url_prefix='/api')
api = Api(class_api)

class ClassAPI:
    class AddClass(Resource):
        @staticmethod
        def post():
            try:
                # Get request body
                body = request.get_json()
                
                if not body or 'period' not in body or 'user' not in body or  'pick' not in body:
                    return {"message": "Invalid request. all 3 categories  are required."}, 400
                
                period = body['period']
                pick = body['pick']
                user = body['user']

                # Create a new period
                new_class = Class(period=period, pick=pick, user=user)
                new_class.create()

                # Return success response
                return new_class.read(), 201
            except Exception as e:
                return {"message": f"Error adding class: {str(e)}"}, 500
            
# READ (GET) - Fetch all classes
        @staticmethod
        def get():
            try:
                classes = Class.query.all()
                return [class_item.read() for class_item in classes], 200
            except Exception as e:
                return {"message": f"Error fetching classes: {str(e)}"}, 500

        # UPDATE (PUT)
        @staticmethod
        def put():
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
        def delete():
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
