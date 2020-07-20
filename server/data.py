import json
import pandas as pd
import numpy as np
import unidecode

from utterances import Utterances


PATH_TO_WIT = "../data/wit/"
PATH_TO_DATA = "../data/fasttext/"

all_data = []
trainings = []
validations = []
counts = {}
valid_counts = {}

def process_string(string):
    return string

def doc_to_train(doc):
    utterance = doc[1]
    intent = doc[0]
    return "__label__" + str(intent).replace("_", "-") + " " + str(utterance)


def split_data(data, counts, ratio):
    train_data = []
    eval_data = []

    valid_counts = {}

    for key, item in counts.items():
        valid_counts[key] = int(item * ratio)
    
    for row in data:
        intent = row[0]
        if valid_counts[intent] > 0:
            eval_data.append(row)
            valid_counts[intent] -= 1
        else:
            train_data.append(row)

    return (train_data, eval_data)


def proccess_row(row, docs, counts):
    intent = row["intent"]
    utterance = row["utterance"]

    if intent not in counts:
        counts[intent] = 0
    
    counts[intent] += 1
    docs.append([intent, utterance])

def process_to_doc(row, docs):
    intent = row["intent"]
    utterance = row["utterance"]

    docs.append({
        "intent": intent,
        "utterance": utterance
    })

def df_to_doc(df):
    """
        Transforms pandas to doc(s): {intent:, uttterance:}
    """
    docs = []
    df.apply(lambda row: process_to_doc(row, docs), axis=1)
    return docs

def df_to_train(df):
    """
        Transforms pandas to doc(s): [intent, uttterance]
        and also couunts the utterances per intent
    """
    docs = []
    counts = {}
    df.apply(lambda row: proccess_row(row, docs, counts), axis=1)
    return docs, counts

def parse_excel(path_to_data, sheet_index, eval_ratio=1/5):
    """
        Parses hand-made excel to trainign and validation files
    """
    df = pd.read_excel(path_to_data, sheet_name=sheet_index)
    # fills missing intents
    df["intent"] = df["intent"].fillna(method="ffill")
    df = df.drop("téma", axis=1)

    # melts data to two columns : [intent, utterance]
    df = pd.melt(df, id_vars="intent", value_name="utterance", var_name="drop")
    df.drop("drop", axis=1, inplace=True)

    df["utterance"] = df["utterance"].str.lower()
    df["intent"] = df["intent"].str.lower()

    df.replace(np.nan, '', regex=True, inplace=True)

    df["utterance"] = df["utterance"].apply(unidecode.unidecode)
    df["intent"] = df["intent"].apply(unidecode.unidecode)

    df.replace('', np.nan, regex=True, inplace=True)
    df.dropna(subset=["utterance"], inplace=True)

    docs = df_to_doc(df)
    
    Utterances().save_utterances(docs)
    
    
def save_files(train_data, eval_data, suffix="data"):
    """
        Save both training and validtation docs to files, ready for model training
    """
    train_name = "{}train_{}.train".format(PATH_TO_DATA, suffix)
    eval_name = "{}train_{}.valid".format(PATH_TO_DATA, suffix)
    
    with open(train_name, 'w', encoding="utf-8") as f:
        for doc in train_data:
            line = doc_to_train(doc)
            f.write(line + "\n")

    with open(eval_name, 'w', encoding="utf-8") as f:
        for doc in eval_data:
            line = doc_to_train(doc)
            f.write(line + "\n")

def parse_wit():
    """
        Parse wit.ai data to training and validation files
    """
    with open(PATH_TO_WIT + "utterances-1.json") as f:
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
            all_data.append([intent, text])

    train_data, eval_data = split_data(all_data, counts, 1/5)
    save_files(train_data, eval_data, suffix="wit")

        
parse_excel("../data/excels/version_1.xlsx", 3, eval_ratio=1/4)