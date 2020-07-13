import json

all_data = []
trainings = []
validations = []
counts = {}
valid_counts = {}

def process_string(string):
    return string

def doc_to_train(doc):
    text = process_string(doc[0])
    intent = process_string(doc[1])
    return "__label__" + str(intent).replace("_", "-") + " " + str(text)


with open("./data/wit/utterances-1.json") as f:
    data = json.load(f)
    utterances = data["utterances"]
    for utterance in utterances:
        if "intent" not in utterance:
            continue
        intent = utterance["intent"]
        text = utterance["text"]

        if intent not in counts:
            counts[intent] = 0
        
        counts[intent] += 1
        all_data.append([text, intent])

for key, item in counts.items():
    valid_counts[key] = int(item * (1/5))

for data in all_data:
    intent = data[1]
    if valid_counts[intent] > 0:
        validations.append(data)
        valid_counts[intent] -= 1
    else:
        trainings.append(data)

with open("./data/fasttext/training_wit.train", 'w', encoding="utf-8") as f:
    for doc in trainings:
        line = doc_to_train(doc)
        f.write(line + "\n")

with open("./data/fasttext/training_wit.valid", 'w', encoding="utf-8") as f:
    for doc in validations:
        line = doc_to_train(doc)
        f.write(line + "\n")

        