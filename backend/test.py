import requests
import sys
from preprocessor import preprocess_data
import pandas as pd


BASE = "http://localhost:5001"


def test_scan(url, expected_status=200):
    r = requests.post(
        f"{BASE}/scan", json={"url": url}, headers={"Content-Type": "application/json"}
    )

    print(f"[{r.status_code}] {url[:60]} -> {r.json()}")
    return r.status_code == expected_status


def compare_features(check_urls_num: int, print_all: bool) -> bool:
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

    df = df.drop(columns="IsLegit")
    # TODO: Exclude cols we have not calcuated yet!
    # print([name for func, name in preprocess_data.func_pointer])
    remaining_col = df.columns.difference(
        other=[name for func, name in preprocess_data.func_pointer]
    )
    # print(remaining_col)
    df: pd.DataFrame = df.drop(columns=remaining_col)

    for i, url in enumerate(urls):
        if i >= check_urls_num:
            break

        # TODO: FIX EITHER THE ORDER OF THE COLUMN OR THE HOW ROWS ARE DELETED
        print(f"URL Number {i + 1}.")

        url_obj = preprocess_data(url)
        url_features = url_obj.get_data()
        url_features_str = url_features.to_string(
            header=False, index=False, float_format="{:.3f}".format
        )
        print(url_features)

        row = df.iloc[[i]]
        print(row)
        row_str = row.to_string(header=False, index=False, float_format="{:.3f}".format)
        print(row_str)

        if url_features_str != row_str:
            if print_all:
                is_same = False
            else:
                return False

    return is_same


compare_features(5, True)
