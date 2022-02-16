import pickle

d = {}
# with open("pickle/sample.pickle", mode="rb") as f:
d = pickle.load(open("pickle/descripter.pickle", mode="rb"))
print(d)