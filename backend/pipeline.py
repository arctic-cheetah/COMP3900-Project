from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
try:
    # Works when running from within `backend/` (e.g. `python3 app.py`).
    from preprocessor import preprocess_data
except ModuleNotFoundError:
    # Works when importing from repo root (namespace package).
    from backend.preprocessor import preprocess_data
from typing import Any


_MODEL_CACHE: dict[str, dict[str, Any]] = {}


def _load_model_bundle(model_path: str) -> dict[str, Any]:
    """Load model + metadata and cache it.

    The current `logit_model.pkl` bundle contains:
    - `model`: a trained LogisticRegression
    - `features`: list of feature column names

    Note: this bundle stores the model trained on raw (unstandardized) features.
    """

    cached = _MODEL_CACHE.get(model_path)
    if cached is not None:
        return cached

    model_dump = joblib.load(model_path)
    if not isinstance(model_dump, dict) or "model" not in model_dump or "features" not in model_dump:
        raise ValueError(
            "Model file must be a dict with keys 'model' and 'features'"
        )

    model: LogisticRegression = model_dump["model"]
    features = model_dump["features"]

    bundle = {"model": model, "features": features}
    _MODEL_CACHE[model_path] = bundle
    return bundle


def run_model(url_features: pd.DataFrame, model_path: str) -> tuple[int, Any]:
    """
    Run pretrained model on features.

    Args:
        url_features (pd.DataFrame): Data frame containing all URL features.
        model_path (str): Path to the saved model.

    Returns:
        tuple: Returns the verdict (safe = 1, phishing = 0) and confidence score.
        Confidence is a 2-element array-like of percentage scores for classes [0, 1].
    """
    try:
        bundle = _load_model_bundle(model_path)
        features = bundle["features"]
        model: LogisticRegression = bundle["model"]
        filtered_url_features = url_features[features]

        is_safe = int(model.predict(filtered_url_features)[0])
        confidence = model.predict_proba(filtered_url_features)[0] * 100.0

        return is_safe, confidence
    except Exception as e:
        print(f'run_model error: "{e}"')
        return (1, [0.0, 100.0])


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
