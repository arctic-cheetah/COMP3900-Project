from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
from Levenshtein import distance, jaro_winkler
from pylcs import lcs_sequence_length

from .preprocessor import preprocess_data


whitelist_path: str = "./ml/data/top_100k_domains.csv"
model_path: str = "./ml/models/logit_model.pkl"


def run_model(url_features: pd.DataFrame, model_path: str) -> tuple[str, str] | None:
    """
    Run pretrained model on features.

    Args:
        url_features (pd.DataFrame): Data frame containing all URL features.
        model_path (str): Path to the saved model.

    Returns:
        tuple: Returns the verdict (safe = 1, phishing = 0) and confidence score.
    """
    try:
        model_dump = joblib.load(model_path)
        features = model_dump["features"]
        model = model_dump["model"]
        
        filtered_url_features = url_features[features]
        is_safe = model.predict(filtered_url_features)[0]
        confidence = model.predict_proba(filtered_url_features)[0] * 100.0

        return is_safe, confidence
    except Exception as e:
        print(f'run_model error: "{e}"')
        return None


#  Where 1 is identical and 0 is different.
def normalised_levenshtein(a: str, b: str):
    return 1 - distance(a, b) / max(len(a), len(b))


#  Where 1 is identical and 0 is different.
def normalised_lcs(a: str, b: str):
    return (2 * lcs_sequence_length(a, b)) / (len(a) + len(b))


def get_whitelist(whitelist_filepath: str):
    whitelist_df = pd.read_csv(whitelist_filepath)
    return whitelist_df["Domain"].tolist()


def search_whitelist(domain: str, whitelist: list):
    whitelist_set = set(whitelist)
    if domain in whitelist_set:
        return {
            "Levenshtein": 1,
            "JaroWinkler": 1,
            "LCS": 1,
        }

    try:
        best_levenshtein = 0
        best_jaro_winkler = 0
        best_lcs = 0
        for whitelist_domain in whitelist:
            best_levenshtein = max(best_levenshtein, normalised_levenshtein(domain, whitelist_domain))
            best_jaro_winkler = max(best_jaro_winkler, jaro_winkler(domain, whitelist_domain))
            best_lcs = max(best_lcs, normalised_lcs(domain, whitelist_domain))

        return {
            "Levenshtein": round(best_levenshtein, 6),
            "JaroWinkler": round(best_jaro_winkler, 6),
            "LCS": round(best_lcs, 6),
        }
    except Exception as e:
        print(e)
        return {
            "Levenshtein": 0,
            "JaroWinkler": 0,
            "LCS": 0,
        }
  

def model_pipeline(url: str) -> tuple[str, str] | None:
    """
    Process URL and runs model.

    Args:
        url (str): URL link to be scanned.
        model_path (str): Path to the saved model.

    Returns:
        tuple: Returns the verdict and confidence score.
    """
    try:
        url_obj = preprocess_data(url)
        df = url_obj.get_data()

        domain = df["RootDomain"].iloc[0]
        whitelist = get_whitelist(whitelist_path)
        scores = search_whitelist(domain, whitelist)
        if scores["Levenshtein"] == 1 and scores["JaroWinkler"] == 1 and scores["LCS"] == 1:
            return 1, [0, 100]

        df["Levenshtein"] = scores["Levenshtein"]
        df["JaroWinkler"] = scores["JaroWinkler"]
        df["LCS"] = scores["LCS"]

        is_safe, confidence = run_model(df, model_path)

        return is_safe, confidence
    except Exception as e:
        print(f'model_pipeline error: "{e}"')
        return None