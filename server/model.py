import fasttext
import json
import string
import random
import sys
import os
import unidecode
import re
from enum import Enum

from threading import Timer

from utterances import Utterances

TEXT = 0
INTENT = 1

TRAIN_OFFSET = 4 # seconds
DATA_PATH = "../data/models/"
N_BACKUP = 10 # number of models to backup
INDEX_LENGTH = 8
MAX_MODEL_SIZE = 5 # in MB

class TRAIN(Enum):
    BAD_INTENT = -2
    NO_TRAIN = -1
    TRAIN_OK = 1

MODEL = {
  "dim": 38,
  "epoch": 500,
  "lr": 0.09,
  "lrUpdateRate": 100,
  "maxn": 6,
  "minCount": 1,
  "minCountLabel": 0,
  "minn": 3,
  "neg": 5,
  "t": 0.0001,
  "wordNgrams": 1,
  "ws": 5
}

EVAL_COUNT = 1


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

        train_path, _ = self.utterances.generate_train_file(eval_count=0)
        MODEL["input"] = train_path
        MODEL["loss"] = "hs"
        self.model = fasttext.train_supervised(
                **MODEL
            )

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


    def scoop_model_params(self):
        train_parameters = [
            'lr',
            'dim',
            'ws',
            'epoch',
            'minCount',
            'minCountLabel',
            'minn',
            'maxn',
            'neg',
            'wordNgrams',
            'bucket',
            'lrUpdateRate',
            't'
        ]

        args_getter = self.model.f.getArgs()

        parameters = {}
        for param in train_parameters:
            attr = getattr(args_getter, param)
            if param == 'loss':
                attr = attr.name
            parameters[param] = attr

        return parameters

    def print_prop(self):
        model = self.model
        f = model.f
        args = f.getArgs()
        keys2 = [a for a in dir(args) if not a.startswith('__')]
        print(keys2)

    def get_models(self):
        meta = self.load_metadata()
        return meta["models"]

    def save(self):
        filename = "model-" + random_string(8) + ".bin"
        self.model.save_model(self.path(filename))
        self.push_model(filename)

    def meta_train(self):
        train_path, eval_path = self.utterances.generate_train_file(eval_count=EVAL_COUNT)
        self.model = fasttext.train_supervised(input=train_path, autotuneValidationFile=eval_path, autotuneModelSize="{}M".format(MAX_MODEL_SIZE))
        self.save()

    def load(self):
        models = self.get_models()
        if len(models) == 0:
            return None
        filename = self.get_models()[-1:][0]
        return fasttext.load_model(self.path(filename))


    def check_intent(self, intent):
        result = re.search(r"^[a-z0-9_]+$", intent)
        return result is not None
    

    def train(self, utterance):
        utterance["index"] = random_string(INDEX_LENGTH)
        utterance["utterance"] = self.process_utterance_text(utterance["utterance"])
        print(utterance)
        intent = utterance["intent"]
        intent = intent.lower()
        if not self.check_intent(intent):
            return (TRAIN.BAD_INTENT, TRAIN.NO_TRAIN)
        utterance["intent"] = intent
        self.utterances.save_utterance(utterance)
        if not self.schedulued_training:
            self.schedulue_training()
        return (TRAIN.TRAIN_OK, TRAIN_OFFSET)

    def just_train(self):
        self.meta_train()