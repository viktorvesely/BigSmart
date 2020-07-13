import fasttext

model = fasttext.train_supervised(input="./data/fasttext/training_wit.train", epoch=500, lr=1)

print("Validation")
print(model.test("./data/fasttext/training_wit.valid"))

print("Interactive mode. Leave by typing '!'")
query = ""
while True:
    query = input()
    if query == "!":
        break
    print(model.predict(query))

print("Cagobelo")