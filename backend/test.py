import requests
import sys
from preprocessor import preprocess_data
import pandas as pd


BASE = "http://localhost:5001"


def test_scan(url, expected_status=200):
    r = requests.post(
        f"{BASE}/scan", json={"url":url}, headers={"Content-Type":"application/json"}
    )

    print(f"[{r.status_code}] {url[:60]} -> {r.json()}")
    return r.status_code == expected_status


def compare_features(check_urls_num : int, print_all : bool) -> bool:
    """
        Compares extracted features from URL to the dataset.
        
        Args:
            check_urls_num (int): Number of URL rows to check.
            print_all (bool): Continue printing all results if features are different.
        
        Returns:
            bool: Returns True if all URL features match, else returns False.
    """
    is_same = True
    df = pd.read_csv("./backend/data/uci_phishing_url_dataset.csv")
    urls = df["URL"]

    df = pd.read_csv("./backend/data/uci_phishing_url_dataset_clean.csv")
    df = df.drop(columns="IsLegit")
    for i, url in enumerate(urls):
        if i >= check_urls_num:
            break
        
        print(f"URL Number {i + 1}.")
        
        url_obj = preprocess_data(url)
        url_features = url_obj.get_data()
        url_features_str = url_features.to_string(header=False, index=False)
        print(url_features_str)
        
        row = df.iloc[[i]]
        row_str = row.to_string(header=False, index=False)
        print(row_str)
        
        if url_features_str != row_str:
            if print_all:
                is_same = False
            else:
                return False

    return is_same

compare_features(5, True)