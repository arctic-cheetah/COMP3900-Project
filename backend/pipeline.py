from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
from preprocessor import preprocess_data


def run_model(url_features: pd.DataFrame, model_path: str) -> tuple[str, str]:
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
        return ("1", "100")


def model_pipeline(url: str, model_path: str) -> tuple[str, str] | None:
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

        is_safe, confidence = run_model(df, model_path)

        return is_safe, confidence
    except Exception as e:
        print(f'model_pipeline error: "{e}"')
        return None
