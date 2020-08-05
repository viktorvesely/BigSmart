from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from model import BigBrain

app = Flask("BigBrain")
CORS(app, resources={r"/*": {"origins": "*"}})
brain = BigBrain()

@app.route("/utterance", methods=['POST'])
def utterance():
    utterance = request.json
    delta = brain.train(utterance)
    return jsonify({
        "train_time": delta 
    })

@app.route("/predict", methods=["POST"])
def predict():
    utterance = request.json
    text = utterance["utterance"]
    intent, confidence = brain.predict(text)
    return jsonify({
        "intent": intent,
        "confidence": confidence
    })

@app.route("/debug")
def debug_command():
    brain.schedulue_training()
    return jsonify({"ok": "ok"})

@app.route("/scoop")
def scoope():
    params = brain.scoop_model_params()
    return jsonify(params)

@app.route("/train")
def train():
    brain.just_train()
    return jsonify({
        "msg": "Lets see the console"
    })

@app.route("/intents")
def intents():
    intents = brain.get_intents()
    return jsonify({
        "intents": intents
    })
