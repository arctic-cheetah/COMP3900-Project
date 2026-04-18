import numpy as np
import pandas as pd
import time
from multiprocessing import Pool, cpu_count
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from ml.preprocessor import preprocess_data
from ml.pipeline import get_whitelist, search_whitelist, run_model

MODEL_RESULTS_FILE = "../outputs/legitphish_dataset_model_results.csv"
VALID_FILE = "../outputs/legitphish_dataset_valid.csv"


def get_result(url):
    whitelist_path = "../data/top_100k_domains.csv"
    model_path = "../models/logit_model.pkl"
    url_obj = preprocess_data(url)
    df = url_obj.get_data()

    domain = df["RootDomain"].iloc[0]
    whitelist = get_whitelist(whitelist_path)
    scores = search_whitelist(domain, whitelist)

    df["Levenshtein"] = scores["Levenshtein"]
    df["JaroWinkler"] = scores["JaroWinkler"]
    df["LCS"] = scores["LCS"]

    is_safe, _ = run_model(df, model_path)

    return url, is_safe

def check_model():
    df = pd.read_csv(VALID_FILE)
    urls = df["url"]
    labels = df["is_legit"]

    model_results = pd.DataFrame(columns=["url", "is_legit", "model_result"])
    try:
        model_results = pd.read_csv(MODEL_RESULTS_FILE)
    except Exception:
        pass

    start_index = len(model_results)
    if start_index == len(df):
        return model_results

    urls = urls[start_index:]
    labels = labels[start_index:]
    with Pool(processes=cpu_count()) as pool:
        start_time = time.time()
        for i, result in enumerate(pool.imap(get_result, urls)):
            url, model_result = result
            model_results.loc[len(model_results)] = [url, labels.iloc[i], model_result]
            if (i + 1) % 100 == 0:
                print(f"\rProcessed {i + 1} in {round(time.time() - start_time, 2)}s", end="")

            if (i + 1) % 1000 == 0:
                model_results.to_csv(MODEL_RESULTS_FILE, index=False)

    model_results.to_csv(MODEL_RESULTS_FILE, index=False)
    return model_results


if __name__ == "__main__":
    results = check_model()

    y_true = results["is_legit"]
    y_pred = results["model_result"]
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"Accuracy score: {accuracy}")
    print(f"Precision score: {precision}")
    print(f"Recall score: {recall}")
    print(f"F1 score: {f1}")

    num_false_positive = sum([1 if row.is_legit == 0 and row.model_result == 1 else 0 for row in results.itertuples()])
    num_false_negative = sum([1 if row.is_legit == 1 and row.model_result == 0 else 0 for row in results.itertuples()])

    print(f"Percentage of phishing URLs classified as legit: {round(num_false_positive / len(results) * 100, 3)}%")
    print(f"Percentage of legit URLs classified as phishing: {round(num_false_negative / len(results) * 100, 3)}%")
