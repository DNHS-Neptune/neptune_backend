from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for demonstration purposes
data_store = []

@app.route('/api/shawn', methods=['GET', 'POST'])
def shawn_endpoint():
    if request.method == 'GET':
        # Respond with the stored data
        return jsonify({"response": data_store}), 200

    elif request.method == 'POST':
        # Parse the incoming JSON data
        content = request.get_json()
        if content:
            data_store.append(content)
            return jsonify({"message": "Data received", "data": content}), 201
        else:
            return jsonify({"error": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True)
