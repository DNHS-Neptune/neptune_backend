from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app, db
from model.themes import Theme

# Create Blueprint and API
theme_api = Blueprint('theme_api', __name__, url_prefix='/api')
api = Api(theme_api)

class ThemeAPI:
    class AddTheme(Resource):
        @staticmethod
        def post():
            try:
                # Get request body
                body = request.get_json()
                
                if not body or 'theme' not in body or 'css' not in body:
                    return {"message": "Invalid request. 'theme' and 'css' are required."}, 400
                
                theme = body['theme']
                css = body['css']

                # Create a new theme
                new_theme = Theme(theme=theme, css=css)
                new_theme.create()

                # Return success response
                return new_theme.read(), 201
            except Exception as e:
                return {"message": f"Error adding theme: {str(e)}"}, 500
# Add the route to the API
api.add_resource(ThemeAPI.AddTheme, '/css/add')
