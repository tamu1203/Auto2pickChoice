import pickle

d = {"name":"ndj", "age":25, "hobby": "YouTube"}
# with open("pickle/sample.pickle", mode="wb") as f:
pickle.dump(d, open("pickle/sample.pickle", mode="wb"))