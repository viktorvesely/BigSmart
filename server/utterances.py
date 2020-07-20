from tinydb import TinyDB, Query, where
from tinyrecord import transaction
import os

PATH_TO_DATA = "../data/intents/intents.json"
OUTPUT_PATH = "../data/fasttext/"
TRAIN = "training.train"
EVAL = "training.valid"



def split_data(data, ratio):
    train_data = []
    eval_data = []
    
    valid_counts = {}
    counts = {}
    
    for utterance in data:
        intent = utterance["intent"]
        if intent not in counts:
            counts[intent] = 0
        counts[intent] += 1
    

    for key, item in counts.items():
        valid_counts[key] = int(item * ratio)
    
    for utterance in data:
        intent = utterance["intent"]
        if valid_counts[intent] > 0:
            eval_data.append(utterance)
            valid_counts[intent] -= 1
        else:
            train_data.append(utterance)

    return (train_data, eval_data)

class Utterances:
    def __init__(self):
        self.db = TinyDB(PATH_TO_DATA)
        self.writing = False

    def get_all(self):
        all_docs = self.db.all()
        return all_docs

    def get_utterances(self, intent):
        Utertance = Query()
        utterances = self.db.search(Utertance.intent == intent)
        return utterances

    def remove_intent(self, intent):
        with transaction(self.db) as tr:
            tr.remove(where("intent") == intent)

    def save_utterance(self, utterance):
        with transaction(self.db) as tr:
            tr.insert(utterance)

    def remove_utterance(self, index):
        with transaction(self.db) as tr:
            tr.remove(where("index") == index)

    def save_utterances(self, utterances):
        with transaction(self.db) as tr:
            tr.insert_multiple(utterances)
    

    def process_doc(self, doc):
        utterance = doc["utterance"]
        intent = doc["intent"]
        return "__label__" + intent.replace("_", "-") + " " + utterance

    def generate_train_file(self, eval_ratio=1/5):
        if self.writing:
            return False
        self.writing = True
        all_utterances = self.get_all()
        train_data, eval_data = split_data(all_utterances, eval_ratio)
        with open(OUTPUT_PATH + TRAIN, 'w+', encoding="utf-8") as f:
            for doc in train_data:
                line = self.process_doc(doc)
                f.write(line + "\n")
        
        with open(OUTPUT_PATH + EVAL, 'w+', encoding="utf-8") as f:
            for doc in eval_data:
                line = self.process_doc(doc)
                f.write(line + "\n")
        self.writing = False
        train_abs = os.path.abspath(OUTPUT_PATH + TRAIN)
        eval_abs = os.path.abspath(OUTPUT_PATH + EVAL)
        return (train_abs, eval_abs)
        
