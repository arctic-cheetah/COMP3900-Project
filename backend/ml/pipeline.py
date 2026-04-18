from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
from Levenshtein import distance, jaro_winkler
from pylcs import lcs_sequence_length
from lime.lime_tabular import LimeTabularExplainer
import re

from ml.preprocessor import preprocess_data

# TODO: Waaah only kelly model's work and not mine after implementing XAI 😭
WHITELIST_PATH: str = "backend/ml/data/top_100k_domains.csv"
# MODEL_PATH: str = "backend/ml/models/random_forest_model.pkl"
# MODEL_PATH: str = "backend/ml/models/logit_model.pkl"
MODEL_PATH: str = "backend/ml/models/logit_model.joblib"

TRAINING_DATA_PATH: str = "backend/ml/models/lime_training_data.joblib"
NUM_TOP_FEATURES = 50

SPECIAL_CONVERSIONS = {
    "no of": "number of",
    "Q mark": "question marks",
    "TLD": "top level domain",
    "levenshtein": "Levenshtein",
    "jaro winkler": "Jaro Winkler",
    "LCS": "longest common subsequence",
}


def run_model(
    url_features: pd.DataFrame, model: LogisticRegression, features: list
) -> tuple[int, float]:
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
        filtered_url_features = url_features[features]
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


#  Where 1 is identical and 0 is different.
def normalised_levenshtein(a: str, b: str):
    return 1 - distance(a, b) / max(len(a), len(b))


#  Where 1 is identical and 0 is different.
def normalised_lcs(a: str, b: str):
    return (2 * lcs_sequence_length(a, b)) / (len(a) + len(b))


def get_whitelist(whitelist_filepath: str):
    whitelist_df = pd.read_csv(whitelist_filepath)
    return whitelist_df["Domain"].tolist()


# helper func to check for subdomain from whitelist
def is_same_domain(domain: str, whitelist_domain: str):
    if domain == whitelist_domain:
        return True
    elif domain.endswith("." + whitelist_domain):
        return True
    else:
        return False


def search_whitelist(domain: str, whitelist: list[str]):
    if domain in whitelist:
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


def remove_is_prefix(string: str, does_have: bool):
    string = string.removeprefix("is ")
    if does_have:
        string = "does have " + string
    else:
        string = "does not have " + string

    return string


def pascal_case_to_text(string: str):
    str_split = re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z][a-z]+|[A-Z]+", string)
    text = " ".join([s if s.upper() == s else s.lower() for s in str_split])

    for k, v in SPECIAL_CONVERSIONS.items():
        text = text.replace(k, v)

    return text


def explanation_to_text(explanation: str):
    explanation_split = explanation.split(" ")
    readable_text = ""
    if len(explanation_split) == 3:
        string = explanation_split[0]
        readable_text = pascal_case_to_text(string)

        inequality = explanation_split[1]
        val = explanation_split[2]
        if inequality == "<=" and float(val) == 0:
            if readable_text.startswith("is "):
                readable_text = remove_is_prefix(readable_text, False)
            else:
                readable_text += " is zero/doesn't exist"
        elif inequality == "<=":
            if readable_text.startswith("is "):
                readable_text = remove_is_prefix(readable_text, True)
            else:
                readable_text += " is shorter/smaller than usual"
        else:
            readable_text += " is longer/bigger than usual"
    elif len(explanation_split) == 5:
        string = explanation_split[2]

        lower_bound = float(explanation_split[0])
        lower_bound = (
            int(lower_bound) if lower_bound.is_integer() else round(lower_bound, 2)
        )
        upper_bound = float(explanation_split[4])
        upper_bound = (
            int(upper_bound) if upper_bound.is_integer() else round(upper_bound, 2)
        )

        readable_text = pascal_case_to_text(string)
        readable_text += f" is between {lower_bound} and {upper_bound}"

    return readable_text


def get_explanations(
    explainer: LimeTabularExplainer,
    url_data: pd.DataFrame,
    model: LogisticRegression,
    features: list,
    is_safe: int,
):
    url_data = url_data[features].iloc[0]
    url_data = url_data.to_numpy()

    explanations = explainer.explain_instance(
        url_data,
        lambda x: model.predict_proba(pd.DataFrame(x, columns=features)),
        num_features=NUM_TOP_FEATURES,
    )

    explanations = explanations.as_list()

    if is_safe == 1:
        explanations = [e[0] for e in explanations if e[1] >= 0]
    else:
        explanations = [e[0] for e in explanations if e[1] < 0]

    top_explanations = explanations[:3]

    top_explanations_filtered = []
    for explanation in top_explanations:
        readable_text = explanation_to_text(explanation)
        top_explanations_filtered.append(readable_text)

    return top_explanations_filtered


def model_pipeline(url: str) -> tuple[int, float] | None:
    """
    Process URL and runs model.

    Args:
        url (str): URL link to be scanned.
        model_path (str): Path to the saved model.

    Returns:
        tuple: Returns the verdict and confidence score.
    """
    try:
        print(f'model_pipeline: checking URL "{url}" with whitelist')
        url_obj = preprocess_data(url)
        url_data = url_obj.get_data()

        domain = url_data["RootDomain"].iloc[0]
        whitelist = get_whitelist(WHITELIST_PATH)
        scores = search_whitelist(domain, whitelist)
        if (
            scores["Levenshtein"] == 1
            and scores["JaroWinkler"] == 1
            and scores["LCS"] == 1
        ):
            print(f'model_pipeline: URL "{url}" is on whitelist')
            return 1, 100.0, ["website found on whitelist"]

        url_data["Levenshtein"] = scores["Levenshtein"]
        url_data["JaroWinkler"] = scores["JaroWinkler"]
        url_data["LCS"] = scores["LCS"]

        print(f'model_pipeline: checking URL "{url}" with model')

        model_dump = joblib.load(MODEL_PATH)

        features = model_dump["features"]
        model = model_dump["model"]
        is_safe, confidence = run_model(url_data, model, features)
        # I realise using LIME means that our model needs to be also updated on the LIME end!
        X_train = joblib.load(TRAINING_DATA_PATH)
        explainer_lime = LimeTabularExplainer(
            X_train.values, feature_names=features, mode="regression", random_state=0
        )
        explanations = get_explanations(
            explainer_lime, url_data, model, features, is_safe
        )

        return is_safe, confidence, explanations
    except Exception as e:
        # Model pipeline error should be flagged as not safe
        print(f'model_pipeline error: "{e}"')
        return None
