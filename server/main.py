from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from model import BigBrain
from model import TRAIN as GYM 

app = Flask("BigBrain")
CORS(app, resources={r"/*": {"origins": "*"}})
brain = BigBrain()

@app.route("/utterance", methods=['POST'])
def utterance():
    utterance = request.json
    res, delta = brain.train(utterance)
    error = False

    if res == GYM.BAD_INTENT:
        error = "Zlý formát intentu. Intent nemôže obsahovať medzery ani špeciálne znaky (okrem '_'), iba písmená a čísla."

    return jsonify({
        "train_time": delta,
        "error": error 
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
