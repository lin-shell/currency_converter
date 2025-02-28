import os
import json

path_data = os.path.join(os.getcwd(), "data")

def load_overwrites():
    with open(os.path.join(path_data, "overwrites.json"), "r") as f:
        return json.load(f)


def save_overwrites(overwrites: dict):
    with open(os.path.join(path_data, "overwrites.json"), "w") as f:
        json.dump(overwrites, f)
