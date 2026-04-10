import numpy as np
import pandas as pd
import requests
import contextlib
import csv
import time

from ml.preprocessor import preprocess_data
from ml.pipeline import get_whitelist, search_whitelist, run_model


TIMEOUT = 2

# def get_result(url):
#     whitelist_path = "../data/top_100k_domains.csv"
#     model_path = "../models/logit_model.pkl"
#     url_obj = preprocess_data(url)
#     df = url_obj.get_data()

#     domain = df["RootDomain"].iloc[0]
#     whitelist = get_whitelist(whitelist_path)
#     scores = search_whitelist(domain, whitelist)

#     df["Levenshtein"] = scores["Levenshtein"]
#     df["JaroWinkler"] = scores["JaroWinkler"]
#     df["LCS"] = scores["LCS"]

#     is_safe, _ = run_model(df, model_path)

#     return is_safe

df = pd.read_csv("../data/legitphish_dataset.csv")
urls = df["URL"]
labels = df["ClassLabel"]

invalid_urls = []
timed_out_urls = []
valid_urls = []
for idx, url in enumerate(urls):
    print(f"Processing {idx}: ", end="")
    start = time.time()

    try:
        r = requests.head(url, allow_redirects=True, timeout=TIMEOUT)
        if r.status_code != 200:
            print(f"Invalid with status code: {r.status_code}")
            invalid_urls.append((url, r.status_code))
            continue
        print(f"Valid URL: {url}")
        valid_urls.append((url, labels.iloc[idx]))
    except requests.exceptions.RequestException as e:
        print(type(e).__name__)
        timed_out_urls.append((url, e))
    except Exception as e:
        print(f"Error: {e}")
        pass
    finally:
        end = time.time()
        print(f" (time take: {end - start})")

with open("../outputs/legitphish_dataset_invalid.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(invalid_urls)

with open("../outputs/legitphish_dataset_timed_out.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(timed_out_urls)

with open("../outputs/legitphish_dataset_valid.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(valid_urls)
