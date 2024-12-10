from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/<name>', methods=['GET'])
def api(name):
    if name == 'nolan':
        return jsonify({
            "name": "Nolan Hightower",
            "age": 15,
            "classes": ["Int 3A", "AP CSP", "AP Sem", "Spanish 5", "AP World"],
            "favorite": {
                "color": "red",
                "number": 32
            }
        })
    elif name == 'kanhay':
        return jsonify({
            "name": "Kanhay Patil",
            "age": 16,
            "classes": ["Honors Principles of Engineering", "Advanced Placement Computer Science Principles", "Advance Placement English Seminar 1", "Advance Placement AP Calculus AB", "Advance Placement Physics C Mechanics"],
            "favorite": {
                "color": "Blue",
                "number": 7
            }
        })
    elif name == 'akshaj':
        return jsonify({
            "name": "Akshaj Gurugugelli",
            "age": 15,
            "classes": ["HPOE", "AP CSP", "World History", "AP Calc", "APES"],
            "favorite": {
                "color": "Blue",
                "number": 1                }
        })
    else:
        return jsonify({
            "error": "that person isnt sigma!"
        })

if __name__ == '__main__':
    app.run(debug=True)