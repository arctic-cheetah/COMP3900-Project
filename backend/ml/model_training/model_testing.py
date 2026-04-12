import numpy as np
import pandas as pd
import requests
import contextlib
import csv
import time


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

    return is_safe
