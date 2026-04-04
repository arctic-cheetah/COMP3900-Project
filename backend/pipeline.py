from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
try:
    # Works when running from within `backend/` (e.g. `python3 app.py`).
    from preprocessor import preprocess_data
except ModuleNotFoundError:
    # Works when importing from repo root (namespace package).
    from backend.preprocessor import preprocess_data
from pathlib import Path
from typing import Any


_MODEL_CACHE: dict[str, dict[str, Any]] = {}


def _load_model_bundle(model_path: str) -> dict[str, Any]:
    """Load model + metadata and cache it.

    The current `logit_model.pkl` bundle contains:
    - `model`: a trained LogisticRegression
    - `features`: list of feature column names

    The LogisticRegression was trained on *standardized* (z-scored) features.
    If the bundle does not include `mu`/`sigma`, we derive them from the
    training CSV and cache them.
    """

    cached = _MODEL_CACHE.get(model_path)
    if cached is not None:
        return cached

    model_dump = joblib.load(model_path)
    if not isinstance(model_dump, dict) or "model" not in model_dump or "features" not in model_dump:
        raise ValueError(
            "Model file must be a dict with keys 'model' and 'features'"
        )

    model = model_dump["model"]
    features = model_dump["features"]

    mu = model_dump.get("mu")
    sigma = model_dump.get("sigma")

    if mu is None or sigma is None:
        data_path = Path(__file__).resolve().parent / "data" / "uci_phishing_url_dataset_clean.csv"
        train = pd.read_csv(data_path)
        mu = train[features].mean()
        sigma = train[features].std(ddof=0).replace(0, 1)

    
    bundle = {"model": model, "features": features, "mu": mu, "sigma": sigma}
    _MODEL_CACHE[model_path] = bundle
    return bundle


def _standardize(url_features: pd.DataFrame, mu: pd.Series, sigma: pd.Series) -> pd.DataFrame:
    """Apply z-score standardization using provided mean/std."""
    numeric = url_features.apply(pd.to_numeric, errors="coerce")
    return (numeric - mu) / sigma


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
        bundle = _load_model_bundle(model_path)
        features = bundle["features"]
        model: LogisticRegression = bundle["model"]
        mu = bundle["mu"]
        sigma = bundle["sigma"]

        print(features)
        filtered_url_features = url_features[features]

        # Model expects standardized features (trained on z-scored inputs).
        standardized = _standardize(filtered_url_features, mu, sigma)

        is_safe = model.predict(standardized)[0]
        confidence = model.predict_proba(standardized)[0] * 100.0

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
