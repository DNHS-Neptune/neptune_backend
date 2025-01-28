from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app, db
from model.themes import Theme

# Create Blueprint and API
theme_api = Blueprint('theme_api', __name__, url_prefix='/api')
api = Api(theme_api)

class ThemeApi(Resource):
    class User(Resource):
        def post(self):
            try:
                # Get request body
                body = request.get_json()
                
                if not body or 'theme' not in body or 'css' not in body:
                    return {"message": "Invalid request. 'theme' and 'css' are required to add."}, 400
                
                theme = body['theme']
                css = body['css']

                # Create a new theme
                new_theme = Theme(theme=theme, css=css)
                new_theme.create()

                # Return success response
                return new_theme.read(), 201
            except Exception as e:
                return {"message": f"Error adding theme: {str(e)}"}, 500        
        def delete(self):
            try:
                body = request.get_json()
                
                if not body or 'theme' not in body:
                    return {"message": "Invalid request. 'theme' is required to delete."}, 400
                
                theme_name = body['theme']
                
                # Find the theme by the provided name
                del_theme = Theme.query.filter_by(_theme=theme_name).first()
                if del_theme:
                    del_theme.delete()
                    return {"message": f"Deleted Theme: {theme_name}"}, 200
                else:
                    return {"message": "Theme not found"}, 404
            except Exception as e:
                return {"message": f"Error unable to delete theme: {str(e)}"}, 500
            
        def put(self):
            try:
                # Parse the JSON body
                body = request.get_json()
                
                # Validate the input
                if not body or 'theme' not in body or 'css' not in body:
                    return {"message": "Invalid request. 'theme' and 'css' are required to update."}, 400
                
                theme_name = body['theme']
                new_css = body['css']
                
                # Find the theme by name
                update_theme = Theme.query.filter_by(_theme=theme_name).first()
                if update_theme:
                    # Use the model's update method to handle updates
                    updated_theme = update_theme.update({'css': new_css})
                    
                    if updated_theme:
                        return {
                            "message": f"Updated Theme: {theme_name} updated_theme: {updated_theme.read()}"}, 200
                else:
                    return {"message": "Theme not found."}, 404
            except Exception as e:
                return {"message": f"Error occurred: {str(e)}"}, 500
        
        def get(self):
            try:
                themes = Theme.query.all()
                return [theme.read() for theme in themes]
            except Exception as e:
                return {"message": f"Error fetching themes: {str(e)}"}, 500

class ThemeReadAPI(Resource):
    def post(self):
        try:
            # Parse the JSON body
            body = request.get_json()
            
            # Validate the input
            if not body or 'theme' not in body :
                return {"message": "Invalid request. 'theme' is required to read."}, 400
            
            theme_name = body['theme']
            
            # Find the theme by name
            read_theme = Theme.query.filter_by(_theme=theme_name).first()
            if read_theme:
                # Use the model's update method to handle updates
                read_theme2 = read_theme.read()  # Returns the full dictionary
                css_value = read_theme2.get('css')  # Extracts only the CSS value

                if read_theme:
                    return {
                        "css":css_value}, 200
            else:
                return {"message": "Theme not found."}, 404
        except Exception as e:
            return {"message": f"Error occurred: {str(e)}"}, 500



# Add the routes to the API
api.add_resource(ThemeApi.User, '/css/crud')
api.add_resource(ThemeReadAPI, '/css/read')


# Ensure this Blueprint is registered in your main application file
