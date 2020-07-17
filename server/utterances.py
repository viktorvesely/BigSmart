from tinydb import TinyDB, Query, where
from tinyrecord import transaction

PATH_TO_DATA = "../data/intents/intents.json"
OUTPUT_PATH = "../data/fasttext/training.train"

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
    

    def process_doc(self, doc):
        utterance = doc["utterance"]
        intent = doc["intent"]
        return "__label__" + intent.replace("_", "-") + " " + utterance

    def generate_train_file(self):
        if self.writing:
            return False
        self.writing = True
        all_utterances = self.get_all()
        with open(OUTPUT_PATH, 'w+', encoding="utf-8") as f:
            for doc in all_utterances:
                line = self.process_doc(doc)
                f.write(line + "\n")
        self.writing = False
        
