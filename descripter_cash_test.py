import pickle

d = {}
d = pickle.load(open("pickle/descripter.pickle", mode="rb"))
print(d)
