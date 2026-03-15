from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd

from preprocessor import preprocess_data


def run_model(url_features : pd.DataFrame, model_path: str) -> tuple[str, str] | None:
    """
    Run pretrained model on features.

    Args:
        url_features (pd.DataFrame): Data frame containing all URL features.
        model_path (str): Path to the saved model.

    Returns:
        tuple: Returns the verdict and confidence score.
    """
    try:
        model = joblib.load(model_path)
        
        # Model returns a np.array
        is_safe = model.predict(df)[0]
        confidence = model.predict_proba(df)[0] * 100.0
        # {notSafe = 0, safe = 1}

        return is_safe, confidence
    except Exception as e:
        print(f'run_model error: "{e}"')
        return None


def model_pipeline(url : str, model_path : str) -> tuple[str, str] | None:
    """
    Process URL and runs model.

    Args:
        url (str): URL link to be scanned.
        model_path (str): Path to the saved model.

    Returns:
        tuple: Returns the verdict and confidence score.
    """
    try:
        url_obj = preprocess_data(sanitised_url)
        df = url_obj.get_data()

        is_safe, confidence = run_model(df, model_path)

        return is_safe, confidence
    
    except Exception as e:
        print(f'model_pipeline error: "{e}"')
        return None