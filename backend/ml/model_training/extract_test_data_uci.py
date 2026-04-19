import pandas as pd
import sys
import os
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, "../")
sys.path.insert(0, "./backend/ml")
sys.path.insert(0, "./backend/ml/model_training")
# from model_training.preprocessor_research_paper import preprocess_data
from preprocessor import preprocess_data
from LCS import get_whitelist, search_whitelist, whitelist_path

# NUM_ROWS = 10
WHICH_DATA = 1
CSV_FILE = "backend/ml/model_training/cleaned_data.csv"
TIMEOUT_EXTRACT_DATA = 5
OUTPUT_CSV = "backend/ml/data/url_test_data_with_feature_var.csv"
PROGRESS_LOG = "backend/ml/model_training/log_extract_progress.txt"


df = pd.read_csv(CSV_FILE, index_col=False)
# Select NUM_ROWS
# select_rows = df.iloc[:NUM_ROWS]

# Run whitelist
get_whitelist(whitelist_path)
whitelist = get_whitelist(whitelist_path)


def process_row(idx: int, row_data: dict, whitelist: list[str]) -> pd.DataFrame | None:
    try:
        url = row_data["URL"]
        # # Check that the url is responsive:
        # try:
        #     res = urlopen(url, timeout=TIMEOUT_EXTRACT_DATA)
        #     if res.getcode() < 400:
        #         print("url is alive!")
        #     else:
        #         return None
        # except Exception:
        #     return None

        out_row_data = preprocess_data(url).get_data()

        domain = out_row_data["RootDomain"].iloc[0]
        scores = search_whitelist(domain, whitelist)

        # Rename the RootDomain to URL
        out_row_data["RootDomain"] = url
        out_row_data.rename(columns={"RootDomain": "URL"}, inplace=True)

        # Add LCS back
        out_row_data["Levenshtein"] = scores["Levenshtein"]
        out_row_data["JaroWinkler"] = scores["JaroWinkler"]
        out_row_data["LCS"] = scores["LCS"]

        # Add isLegit back
        out_row_data["IsLegit"] = row_data["IsLegit"]
        return out_row_data
    except Exception:
        return None


def build_test_data(rows: list[pd.DataFrame]) -> pd.DataFrame:
    if rows:
        test_data = pd.concat(rows, ignore_index=True)
    else:
        test_data = pd.DataFrame()

    if not test_data.empty:
        test_data.reset_index(drop=True, inplace=True)
        if "Unnamed: 0" in test_data.columns:
            test_data.drop(columns=["Unnamed: 0"], inplace=True)

    return test_data


def save_partial(rows: list[pd.DataFrame], output_csv: str) -> None:
    test_data = build_test_data(rows)
    if test_data.empty:
        return

    output_dir = os.path.dirname(output_csv)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    test_data.to_csv(output_csv, index=False)


def log_progress(completed: int, total: int, log_path: str) -> None:
    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"Processed {completed}/{total} URLs\n")


records = df.to_dict(orient="records")
total = len(records)
completed = 0
test_rows: list[pd.DataFrame] = []

max_workers = 10
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [
        executor.submit(process_row, idx, row_data, whitelist)
        for idx, row_data in enumerate(records)
    ]
    for future in as_completed(futures):
        result = future.result()
        if result is not None:
            test_rows.append(result)
        completed += 1
        if completed % 1000 == 0 or completed == total:
            log_progress(completed, total, PROGRESS_LOG)
            print(f"Processed {completed}/{total} URLs")
            save_partial(test_rows, OUTPUT_CSV)

test_data = build_test_data(test_rows)
if not test_data.empty:
    test_data.to_csv(OUTPUT_CSV, index=False)
print(test_data)
