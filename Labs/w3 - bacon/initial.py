import pickle

if __name__ == "__main__":
    with open("resources/names.pickle", "rb") as f:
        names = pickle.load(f)
