from flask import Flask
from flask import request
from flask import jsonify

from model import BigBrain

app = Flask("BigBrain")
brain = BigBrain()

@app.route('/')
def hello_world():
    return 'Hello, World!'

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