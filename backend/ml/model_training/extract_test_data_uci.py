import pandas as pd
import sys
from urllib.request import urlopen

sys.path.insert(0, "../")
sys.path.insert(0, "./backend/ml")
sys.path.insert(0, "./backend/ml/model_training")
# from model_training.preprocessor_research_paper import preprocess_data
from preprocessor import preprocess_data
from LCS import get_whitelist, search_whitelist, whitelist_path

NUM_ROWS = 40
WHICH_DATA = 1
CSV_FILE = "backend/ml/data/phishing_site_urls.csv"
# CSV_FILE = "backend/ml/data/StealthPhisher2025.csv"
TIMEOUT_EXTRACT_DATA = 5


df = pd.read_csv(CSV_FILE, index_col=False)
# randomise data
df = df.sample(frac=1, ignore_index=True)
# Convert label from bad = 0 and safe = 1
df["Label"] = df["Label"].map({"bad": 0, "good": 1})
# df["Label"] = df["Label"].map({"Phishing": 0, "Legitimate": 1})

# Obtain a subset of the data
df = df[["URL", "Label"]]

## Rename the column `Label` to is `IsLegit`
df.rename(columns={"Label": "IsLegit"}, inplace=True)
# Select NUM_ROWS
select_rows = df.iloc[:NUM_ROWS]


# Run whitelist
get_whitelist(whitelist_path)
whitelist = get_whitelist(whitelist_path)

test_data: pd.DataFrame = pd.DataFrame()
for idx, row_data in select_rows.iterrows():
    row_data["URL"] = "https://" + row_data["URL"]
    # all urls are missing 'https://' add it back
    print(f"Doing {idx}, URL: {row_data["URL"]}")
    # Check that the url is responsive:
    try:
        res = urlopen(row_data["URL"], timeout=TIMEOUT_EXTRACT_DATA)
        if res.getcode() < 400:
            print("url is alive!")
        else:
            continue
    except Exception as e:
        print(e)
        continue

    out_row_data = preprocess_data(row_data["URL"]).get_data()

    domain = out_row_data["RootDomain"].iloc[0]
    # print(domain)
    scores = search_whitelist(domain, whitelist)

    # Rename the RootDomain to URL
    out_row_data["RootDomain"] = row_data["URL"]
    out_row_data.rename(columns={"RootDomain": "URL"}, inplace=True)

    # Add LCS back
    out_row_data["Levenshtein"] = scores["Levenshtein"]
    out_row_data["JaroWinkler"] = scores["JaroWinkler"]
    out_row_data["LCS"] = scores["LCS"]

    # Add isLegit back
    out_row_data["IsLegit"] = row_data["IsLegit"]

    if idx == 0:
        test_data = out_row_data
        continue
    test_data = pd.concat([test_data, out_row_data], ignore_index=True)
    # print(test_data)


test_data.reset_index(drop=True, inplace=True)
if "Unnamed: 0" in test_data.columns:
    test_data.drop(columns=["Unnamed: 0"], inplace=True)

test_data.to_csv("backend/ml/data/url_test_data_compatible.csv", index=False)
print(test_data)
