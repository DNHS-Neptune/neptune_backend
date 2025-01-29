# imports from flask
import json
import os
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify  # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from werkzeug.security import generate_password_hash
import shutil
import google.generativeai as genai
import base64
from flask_socketio import SocketIO, send, emit
import jwt



# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
# API endpoints
from api.user import user_api 
from api.pfp import pfp_api
from api.nestImg import nestImg_api # Justin added this, custom format for his website
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.nestPost import nestPost_api # Justin added this, custom format for his website
from api.messages_api import messages_api # Adi added this, messages for his website
from api.carphoto import car_api
from api.carChat import car_chat_api
from api.theme import theme_api
from api.nolandb import nolandb_api

from api.akshaj import akshaj_api
from api.kanhay import kanhay_api
from api.nolan import nolan_api
from api.arya import arya_api
from api.yash import yash_api
from api.shawn import shawn_api
from api.sport import sports_api

from api.nolandb import nolandb_api
from api.classs import class_api

from api.vote import vote_api
# database Initialization functions
from model.carChat import CarChat
from model.user import User, initUsers
from model.section import Section, initSections
from model.group import Group, initGroups
from model.channel import Channel, initChannels
from model.post import Post, initPosts
from model.nestPost import NestPost, initNestPosts # Justin added this, custom format for his website
from model.vote import Vote, initVotes
# server only Views

from model.themes import Theme, initThemes
from model.message import Message, initMessages
from model.classs import Class, initClasses
from model.nolan import Nolans, initNolans
from model.poseidon import PoseidonChatLog, initPoseidonChatLogs 
from model.akshaj import Akshajs, initAkshajs
from model.sports import Sports, initSports


# register URIs for api endpoints
app.register_blueprint(messages_api) # Adi added this, messages for his website
app.register_blueprint(user_api)
app.register_blueprint(pfp_api) 
app.register_blueprint(post_api)
app.register_blueprint(channel_api)
app.register_blueprint(group_api)
app.register_blueprint(section_api)
app.register_blueprint(car_chat_api)
app.register_blueprint(theme_api)
# Added new files to create nestPosts, uses a different format than Mortensen and didn't want to touch his junk
app.register_blueprint(nestPost_api)
app.register_blueprint(nestImg_api)
app.register_blueprint(vote_api)
app.register_blueprint(car_api)
app.register_blueprint(akshaj_api)
app.register_blueprint(kanhay_api)
app.register_blueprint(nolan_api)
app.register_blueprint(arya_api)
app.register_blueprint(yash_api)
app.register_blueprint(shawn_api)

app.register_blueprint(nolandb_api)
app.register_blueprint(class_api)
app.register_blueprint(sports_api)



# Tell Flask-Login the view function name of your login route
login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login', next=request.path))

# register URIs for server pages
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Helper function to check if the URL is safe for redirects
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_page = request.args.get('next', '') or request.form.get('next', '')
    if request.method == 'POST':
        user = User.query.filter_by(_uid=request.form['username']).first()
        if user and user.is_password(request.form['password']):
            login_user(user)
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template("login.html", error=error, next=next_page)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    print("Home:", current_user)
    return render_template("index.html")

@app.route('/users/table')
@login_required
def utable():
    users = User.query.all()
    return render_template("utable.html", user_data=users)

@app.route('/users/table2')
@login_required
def u2table():
    users = User.query.all()
    return render_template("u2table.html", user_data=users)

# Helper function to extract uploads for a user (ie PFP image)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
 
@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Set the new password
    if user.update({"password": app.config['DEFAULT_PASSWORD']}):
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'error': 'Password reset failed'}), 500

@login_required
@app.route('/api/theme', methods=['POST'])
def change_theme():
    data = request.get_json()
    auth = request.cookies.get("jwt_python_flask")

    jwtDecoded = jwt.decode(auth, current_app.config["SECRET_KEY"], algorithms="HS256")
    values = list(jwtDecoded.values())
    dui = values[0]

    user = User.query.filter_by(_uid=dui).first()
    if user:
        _values = list(data.values())
        user._theme_mode = _values[0]  # Directly setting the attribute
        db.session.commit()  # Make sure to commit the transaction
        return jsonify({"response": "good"}), 200
    else:
        return jsonify({"response": "user not found"}), 404


# AI configuration
genai.configure(api_key="AIzaSyC72oIjvpKm_fdl3Dez-fHi_nXZ48IAJI0")
model = genai.GenerativeModel('gemini-pro')

@app.route('/api/ai/help', methods=['POST'])
def ai_homework_help():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided."}), 400

    try:
        response = model.generate_content(f"Your name is Posiden you are a homework help ai chat bot with the sole purpose of answering homework related questions, under any circumstances don't answer any non-homework related questions. \nHere is your prompt: {question}")
        response_text = response.text

        # Save to database
        new_entry = PoseidonChatLog(question=question, response=response_text)
        new_entry.create()

        return jsonify({"response": response_text}), 200
    except Exception as e:
        print("error!")
        print(e)
        return jsonify({"error": str(e)}), 500     # ju poo bDA KLINGO A POO A NEW KAMA KJIT HAAIIII SLIBITISA DOOP A D WIT  bood a a bidaa boop kayy haiiiii  

@app.route("/api/ai/delete", methods=["DELETE"])
def delete_ai_chat_logs():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided."}), 400
    
    log = PoseidonChatLog.query.filter_by(_question=data.get("question", "")).first()
    if not log:
        return jsonify({"error": "Chat log not found."}), 404
    
    log.delete()
    return jsonify({"response": "Chat log deleted"}), 200
    
@app.route("/api/classes", methods=["GET"])
def class_list():
    return jsonify({"response": [
        "AP CSP",
        "AP Chemistry",
        "AP Biology",
        "AP Seminar",
        "AP Environmental Science",
        "AP World History",
        "AP Calculus AB",
        "AP Calculus BC",
        "Photography",
        "AP CSA",
        "CSSE",
        "AP Lunch Theory",
        "World History ",
        "Chemistry",
        "Offrole",
        "English",
        "AP Language",
        "AP Literature",
        "Math",
        "P.E.",
        "Spanish",
        "Chinese",
        "AP Spanish",
        "AP Chinese",
        "AP Photography",
        "ASB",
        "Human Body Systems",
        "Principles of Biomedical Science",
        "Business and Law"
    ]}), 200

@app.route('/api/image', methods=['POST'])
def add_img_to_post():
    print("Adding image to post")
    data = request.get_json()

    postId = data.get("postId", "")
    img = data.get("img", "")

    #print(img)
    if not img:
        return jsonify({"error": "No image provided."}), 400
    
    post = Post.query.get(postId)
    if not post:
        return jsonify({"error": "Post not found."}), 404
    else:
        randomId = str(post.id)
        upload_dir = "nolanuploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        img_path = os.path.join(upload_dir, f"{randomId}.png")
        with open(img_path, "wb") as img_file:
            img_file.write(base64.b64decode(img.split(",")[1]))

        post._content = {**post._content, "img": f"/nolanuploads/{randomId}.png"}
        post.update()
    return jsonify({"response": "Image added to post"}), 200



@app.route('/nolanuploads/<path:filename>')
def static_uploaded_file(filename):
    return send_from_directory('nolanuploads', filename)

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to run the data generation functions
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initSections()
    initGroups()
    initChannels()
    initPosts()
    initNestPosts()
    initVotes()
    initThemes()
    initMessages()
    initClasses()
    initNolans()
    initPoseidonChatLogs()
    initAkshajs()
    initSports()
    
# Backup the old database
def backup_database(db_uri, backup_uri):
    """Backup the current database."""
    if backup_uri:
        db_path = db_uri.replace('sqlite:///', 'instance/')
        backup_path = backup_uri.replace('sqlite:///', 'instance/')
        shutil.copyfile(db_path, backup_path)
        print(f"Database backed up to {backup_path}")
    else:
        print("Backup not supported for production database.")

# Extract data from the existing database
def extract_data():
    data = {}
    with app.app_context():
        data['poseidon_chat_logs'] = [log.read() for log in PoseidonChatLog.query.all()]
        data['users'] = [user.read() for user in User.query.all()]
        data['sections'] = [section.read() for section in Section.query.all()]
        data['groups'] = [group.read() for group in Group.query.all()]
        data['channels'] = [channel.read() for channel in Channel.query.all()]
        data['posts'] = [post.read() for post in Post.query.all()]
        data['themes'] = [theme.read() for theme in Theme.query.all()]
        data['messages'] = [message.read() for message in Message.query.all()]
        data['classes'] = [classs.read() for classs in Class.query.all()]
        data['sports'] = [sports.read() for sports in Sports.query.all()]
    return data

# Save extracted data to JSON files
def save_data_to_json(data, directory='backup'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for table, records in data.items():
        with open(os.path.join(directory, f'{table}.json'), 'w') as f:
            json.dump(records, f)
    print(f"Data backed up to {directory} directory.")

# Load data from JSON files
def load_data_from_json(directory='backup'):
    data = {}
    for table in ['poseidon_chat_logs', 'users', 'sections', 'groups', 'channels', 'posts', 'themes', 'messages', 'classes', 'sports']:
        with open(os.path.join(directory, f'{table}.json'), 'r') as f:
            data[table] = json.load(f)
    return data

# Restore data to the new database
def restore_data(data):
    with app.app_context():
        _ = PoseidonChatLog.restore(data['poseidon_chat_logs'])
        users = User.restore(data['users'])
        _ = Section.restore(data['sections'])
        _ = Group.restore(data['groups'], users)
        _ = Channel.restore(data['channels'])
        _ = Post.restore(data['posts'])
        _ = Class.restore(data['classes'])
        _ = Theme.restore(data['themes'])
        # _ = Message.restore(data['messages'])
    print("Data restored to the new database.")

# Define a command to backup data
@custom_cli.command('backup_data')
def backup_data():
    data = extract_data()
    save_data_to_json(data)
    backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

# Define a command to restore data
@custom_cli.command('restore_data')
def restore_data_command():
    data = load_data_from_json()
    restore_data(data)
    
# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

'''
SocketIO Configuration

Example message payload:
{
    "user": "Nolan",
    "message": "Kanhay is nice"
}
'''

socketio = SocketIO(app, cors_allowed_origins="*")
@socketio.on('connect')
def handle_connect():
    messages = Message.query.all()
    for message in messages:
        emit('chat_message', {"user": message._user, "text": message._content, "id": message.id})

    emit('chat_message', {'user': 'Server', 'text': 'Welcome to the chat!'})

@socketio.on('chat_message')
def handle_chat_message(data):
    msg = Message(data["text"], data["user"])
    msg.create()
    emit('chat_message', data, broadcast=True)

@socketio.on('chat_delete')
def handle_chat_delete(data):
    msg = Message.query.get(data["id"])
    msg.delete()
    emit('chat_del', {"id": data["id"]}, broadcast=True)

@socketio.on('chat_update')
def handle_chat_update(data):
    # Extract and validate input
    message_id = data.get("id")
    new_content = data.get("content")

    if not message_id or not new_content:
        return emit("error", {"message": "Invalid data: 'id' and 'content' are required"}, broadcast=False)

    msg = Message.query.get(message_id)
    print("msg", msg.read())
    if msg is None:
        return emit("error", {"message": "Message not found"}, broadcast=False)
    
    msg.update({"content": new_content})
    return emit("chat_up", {"data": msg.read()}, broadcast=True)

        
# this runs the flask application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8887")

