import numpy as np
import pandas as pd
import requests
import os
import time
from multiprocessing import Pool, cpu_count

from ml.preprocessor import preprocess_data
from ml.pipeline import get_whitelist, search_whitelist, run_model


TIMEOUT = 4
DATA_FILE = "../data/legitphish_dataset.csv"
INVALID_FILE = "../outputs/legitphish_dataset_invalid.csv"
TIMED_OUT_FILE = "../outputs/legitphish_dataset_timed_out.csv"
VALID_FILE = "../outputs/legitphish_dataset_valid.csv"

invalid_urls = pd.DataFrame(columns=["url", "status_code"])
timed_out_urls = pd.DataFrame(columns=["url", "error"])
valid_urls = pd.DataFrame(columns=["url", "is_legit"])

def test_url(url, label):
    try:
        r = requests.head(url, allow_redirects=True, timeout=TIMEOUT)
        if r.status_code != 200:
            # print(f"Invalid with status code: {r.status_code}")
            return ("invalid", url, r.status_code)
        else:
            # print(f"Valid URL: {url}")
            return ("valid", url, label)
    except Exception as e:
        # print(type(e).__name__)
        # print(f"Error: {e}")
        return ("timeout", url, str(e))


def test_url_unpack(args):
    return test_url(*args)


if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE)
    urls = df["URL"]
    labels = df["ClassLabel"]

    if os.path.exists(INVALID_FILE) and os.path.exists(TIMED_OUT_FILE) and os.path.exists(VALID_FILE):
        try:
            invalid_urls = pd.read_csv(INVALID_FILE)
        except pd.errors.EmptyDataError:
            pass

        try:
            timed_out_urls = pd.read_csv(TIMED_OUT_FILE)
        except pd.errors.EmptyDataError:
            pass

        try:
            valid_urls = pd.read_csv(VALID_FILE)
        except pd.errors.EmptyDataError:
            pass

    start_index = len(invalid_urls) + len(timed_out_urls) + len(valid_urls)
    urls = urls[start_index:]
    labels = labels[start_index:]
    tasks = list(zip(urls, labels))
    with Pool(processes=cpu_count()) as pool:
        start_time = time.time()
        for i, result in enumerate(pool.imap(test_url_unpack, tasks)):
            result_type, url, value = result

            if result_type == "invalid":
                invalid_urls.loc[len(invalid_urls)] = [url, value]
            elif result_type == "timeout":
                timed_out_urls.loc[len(timed_out_urls)] = [url, value]
            elif result_type == "valid":
                valid_urls.loc[len(valid_urls)] = [url, value]

            if i % 100 == 0 and i > 0:
                print("\033[K", end="")
                print(f"Processed {start_index + i} in {round(time.time() - start_time)}s")
                print("\033[K", end="")
                print(f"\tInvalid urls: {len(invalid_urls)}")
                print("\033[K", end="")
                print(f"\tTimed Out urls: {len(timed_out_urls)}")
                print("\033[K", end="")
                print(f"\tValid urls: {len(valid_urls)}")
                print("\033[4F", end="")

            if i % 1000 == 0 and i > 0:
                invalid_urls.to_csv(INVALID_FILE, index=False)
                timed_out_urls.to_csv(TIMED_OUT_FILE, index=False)
                valid_urls.to_csv(VALID_FILE, index=False)
