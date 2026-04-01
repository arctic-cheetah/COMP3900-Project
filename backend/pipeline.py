from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
from preprocessor import preprocess_data
from Levenshtein import distance, jaro_winkler
from pylcs import lcs_sequence_length


whitelist_path: str = "./data/top_100k_domains.csv"
model_path: str = "./models/logit_model.pkl"


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
def normalised_levenshtein(a, b):
    return 1 - distance(a, b) / max(len(a), len(b))


#  Where 1 is identical and 0 is different.
def normalised_lcs(a, b):
    return (2 * lcs_sequence_length(a, b)) / (len(a) + len(b))


def search_whitelist(domain: str, whitelist_filepath: str):
    whitelist_file = pd.read_csv(whitelist_filepath)
    whitelist = whitelist_file["Domain"]

    best_levenshtein = 0
    best_jaro_winkler = 0
    best_lcs = 0
    for whitelist_domain in whitelist:
        try:
            best_levenshtein = max(best_levenshtein, normalised_levenshtein(domain, whitelist_domain))
            best_jaro_winkler = max(best_jaro_winkler, jaro_winkler(domain, whitelist_domain))
            best_lcs = max(best_lcs, normalised_lcs(domain, whitelist_domain))
        except Exception as e:
            print(e)

    return {
        "Levenshtein": best_levenshtein,
        "JaroWinkler": best_jaro_winkler,
        "LCS": best_lcs,
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
        scores = search_whitelist(domain, whitelist_path)
        if (scores["Levenshtein"] == 1 and scores["JaroWinkler"] == 1 and scores["LCS"] == 1):
            return 1, [0, 100]
            
        is_safe, confidence = run_model(df, model_path)

        return is_safe, confidence
    except Exception as e:
        print(f'model_pipeline error: "{e}"')
        return None