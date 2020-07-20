import fasttext
import json
import string
import random
import sys
import os
import unidecode

from threading import Timer

from utterances import Utterances

TEXT = 0
INTENT = 1

TRAIN_OFFSET = 4 # seconds
DATA_PATH = "../data/models/"
N_BACKUP = 10 # number of models to backup
INDEX_LENGTH = 8

LR = 1.0
EPOCH = 2000

def log(msg):
    print(msg, file=sys.stderr)


def random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def label_to_intent(label):
    processed = label.replace("__label__", "")
    return processed.replace("-", "_")

class BigBrain:
    def __init__(self):
        self.utterances = Utterances()
        self.ongoing_training = False
        self.schedulued_training = False
        self.repeat_training = False
        self.model = self.load()
        self.training_stack = []

    def schedulue_training(self):
        if self.schedulued_training:
            self.repeat_training = True
            return False
        self.schedulued_training = True
        t = Timer(TRAIN_OFFSET, self.gym)
        t.start()
        return True

    def process_utterance_text(self, text):
        processed = unidecode.unidecode(text)
        processed = processed.lower()
        return processed

    def predict(self, utterance):
        if self.model is None:
            print("Model is not initialized yet")
            return None, 0
        processed = self.process_utterance_text(utterance)
        response = self.model.predict(processed)
        if len(response) < 2:
            return None, 0
        confidence = response[1][0]
        intent = label_to_intent(response[0][0])
        return (intent, confidence)

    def gym(self):
        if self.ongoing_training:
            # reschedule training
            self.schedulue_training()
            return

        self.ongoing_training = True

        train_path, _ = self.utterances.generate_train_file(eval_ratio=0)
        self.model = fasttext.train_supervised(input=train_path, lr=LR, epoch=EPOCH)

        self.schedulued_training = False
        self.ongoing_training = False

        self.save()

        if self.repeat_training:
            self.repeat_training = False
            self.gym()

    def path(self, name):
        return DATA_PATH + name

    def create_metadata(self):
        save = None
        with open(self.path("meta.json"), 'w+', encoding="utf-8") as f:
            save = {
                "models": []
            }
            json.dump(save, f)
        return save

    def load_metadata(self):
        meta = None
        with open(self.path("meta.json")) as f:
            meta = json.load(f)
        return meta

    def push_model(self, filename):
        meta = self.load_metadata()
        if (len(meta["models"]) == N_BACKUP):
            to_delete = meta["models"][:1][0]
            os.remove(self.path(to_delete))
            meta["models"] = meta["models"][1:]
        meta["models"].append(filename)
        with open(self.path("meta.json"), 'w+', encoding="utf-8") as f:
            json.dump(meta, f)
    
    def get_intents(self):
        labels = self.model.get_labels()
        intents = []
        for label in labels:
            intents.append(label_to_intent(label))
        return intents

    def get_models(self):
        meta = self.load_metadata()
        return meta["models"]

    def save(self):
        filename = "model-" + random_string(8) + ".bin"
        self.model.save_model(self.path(filename))
        self.push_model(filename)

    def meta_train(self):
        train_path, eval_path = self.utterances.generate_train_file(eval_ratio=1/5)
        self.model = fasttext.train_supervised(input=train_path, autotuneValidationFile=eval_path)

    def load(self):
        models = self.get_models()
        if len(models) == 0:
            return None
        filename = self.get_models()[-1:][0]
        return fasttext.load_model(self.path(filename))

    def train(self, utterance):
        utterance["index"] = random_string(INDEX_LENGTH)
        utterance["utterance"] = self.process_utterance_text(utterance["utterance"])
        self.utterances.save_utterance(utterance)
        if not self.schedulued_training:
            self.schedulue_training()
        return TRAIN_OFFSET

    def just_train(self):
        self.meta_train()