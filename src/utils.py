import json
import pandas as pd


def load_corpus(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_test(path):
    with open(path, "r") as f:
        return json.load(f)


def save_results(results, path):
    df = pd.DataFrame(results)
    df.to_csv(path, index=False)