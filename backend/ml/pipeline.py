import joblib
import pandas as pd
from Levenshtein import distance, jaro_winkler
from pylcs import lcs_sequence_length

try:
    from .preprocessor import preprocess_data
except ImportError:
    from preprocessor import preprocess_data

whitelist_path: str = "backend/ml/data/top_100k_domains.csv"
model_path: str = "backend/ml/models/logit_model.pkl"
URL_FEATURE_WEIGHT = 0.3
HTML_FEATURE_WEIGHT = 1e2


def run_model(url_features: pd.DataFrame, model_filepath: str) -> tuple[int, float]:
    """
    Run pretrained model on features.

    Args:
        url_features (pd.DataFrame): Data frame containing all URL features.
        model_path (str): Path to the saved model.

    Returns:
        tuple: Returns the verdict (safe = 1, phishing = 0) and confidence score.
    """
    try:
        # TODO: WHY THE ARE WE ALWAYS LOADING THE MODEL EACH TIME IT SCANS
        # A URL? JUST CACHE IT
        model_dump = joblib.load(model_filepath)
        features = model_dump["features"]
        model = model_dump["model"]

        filtered_url_features = url_features.reindex(columns=features, fill_value=0)
        is_safe: int = model.predict(filtered_url_features)[0].item()
        # Model actually outputs an np array of prob
        # of confidence
        # So just get the float of confidence
        confidence_val_safe_and_not_safe = model.predict_proba(filtered_url_features)[0]
        confidence: float = confidence_val_safe_and_not_safe[0].item() * 100

        return is_safe, confidence
    except Exception as e:
        print(f'run_model error: "{e}"')
        return 0, 100.0


def get_safe_probability(
    model, features_df: pd.DataFrame, expected_features: list[str]
) -> float:
    aligned_features = features_df.reindex(columns=expected_features, fill_value=0)
    probabilities = model.predict_proba(aligned_features)[0]

    # if hasattr(model, "classes_") and 1 in model.classes_:
    #     safe_index = list(model.classes_).index(1)
    #     return float(probabilities[safe_index])

    # if len(probabilities) > 1:
    #     return float(probabilities[1])

    return float(probabilities[0])


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
            best_levenshtein = max(
                best_levenshtein, normalised_levenshtein(domain, whitelist_domain)
            )
            best_jaro_winkler = max(
                best_jaro_winkler, jaro_winkler(domain, whitelist_domain)
            )
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


def model_pipeline(
    url: str, feature_mode: str = "domain_only"
) -> tuple[int, float] | None:
    """
    Process URL and runs model.

    Args:
        url (str): URL link to be scanned.
        model_path (str): Path to the saved model.

    Returns:
        tuple: Returns the verdict and confidence score.
    """
    try:
        model_dump = joblib.load(model_path)
        features = model_dump["features"]
        model = model_dump["model"]

        if feature_mode == "domain_only":
            url_obj = preprocess_data(url, feature_mode="domain_only")
            df = url_obj.get_data()
            safe_probability = get_safe_probability(model, df, features)
        elif feature_mode == "full":
            url_obj = preprocess_data(url, feature_mode="full")
            df = url_obj.get_data()
            safe_probability = get_safe_probability(model, df, features)
        else:
            url_obj = preprocess_data(url, feature_mode="domain_only")
            url_df = url_obj.get_data()

            html_obj = preprocess_data(url, feature_mode="full")
            html_df = html_obj.get_data()

            url_safe_probability = get_safe_probability(model, url_df, features)
            html_safe_probability = get_safe_probability(model, html_df, features)
            safe_probability = (
                URL_FEATURE_WEIGHT * url_safe_probability
                + HTML_FEATURE_WEIGHT * html_safe_probability
            )

            print(safe_probability)
            df = html_df if HTML_FEATURE_WEIGHT >= URL_FEATURE_WEIGHT else url_df
        domain = df["RootDomain"].iloc[0]
        whitelist = get_whitelist(whitelist_path)
        scores = search_whitelist(domain, whitelist)
        if (
            scores["Levenshtein"] == 1
            and scores["JaroWinkler"] == 1
            and scores["LCS"] == 1
        ):
            return 1, 100.0

        is_safe = 1 if safe_probability >= 0.5 else 0
        confidence = round(
            (safe_probability if is_safe else 1 - safe_probability) * 100, 2
        )

        return is_safe, confidence
    except Exception as e:
        # Model pipeline error should be flagged as not safe
        print(f'model_pipeline error: "{e}"')
        return None
