from flask import Flask, request, jsonify
from threading import Lock

app = Flask(__name__)

human_command = None
robot_response = None
lock = Lock()

@app.route("/command", methods=["POST"])
def receive_command():
    global human_command
    with lock:
        human_command = request.json["text"]
    return jsonify({"status": "ok"})

@app.route("/command", methods=["GET"])
def get_command():
    global human_command
    with lock:
        if human_command:
            cmd = human_command
            human_command = None
            return jsonify({"text": cmd})
        else:
            return jsonify({"text": None})

@app.route("/response", methods=["POST"])
def receive_response():
    global robot_response
    with lock:
        robot_response = request.json["text"]
    return jsonify({"status": "ok"})

@app.route("/response", methods=["GET"])
def get_response():
    global robot_response
    with lock:
        if robot_response:
            r = robot_response
            robot_response = None
            return jsonify({"text": r})
        else:
            return jsonify({"text": None})

if __name__ == "__main__":
    app.run(port=5000)
