import os
import sys
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
from preprocessor import preprocess_data

STEALTH_PATH = "backend/ml/data/StealthPhisher2025.csv"
OUTPUT_PATH = "backend/ml/data/stealthphisher2025_uci_columns.csv"

STEALTH_TO_UCI = {
    "URL": "URL",
    "LengthOfURL": "URLLength",
    "DomainLengthOfURL": "DomainLength",
    "IsDomainIP": "IsDomainIP",
    "TLDLength": "TLDLength",
    "NumberOfSubdomains": "NoOfSubDomain",
    "LetterCntInURL": "NoOfLettersInURL",
    "URLLetterRatio": "LetterRatioInURL",
    "DigitCntInURL": "NoOfDigitsInURL",
    "URLDigitRatio": "DigitRatioInURL",
    "EqualCharCntInURL": "NoOfEqualsInURL",
    "QuesMarkCntInURL": "NoOfQMarkInURL",
    "AmpCharCntInURL": "NoOfAmpersandInURL",
    "OtherSpclCharCntInURL": "NoOfOtherSpecialCharsInURL",
    "URLOtherSpclCharRatio": "SpecialCharRatioInURL",
    "HasSSL": "IsHTTPS",
    "LineOfCode": "LineOfCode",
    "LongestLineLength": "LargestLineLength",
    "HasTitle": "HasTitle",
    "HasFavicon": "HasFavicon",
    "HasRobotsBlocked": "Robots",
    "IsResponsive": "IsResponsive",
    "HasIFrame": "NoOfiFrame",
    "HasSocialMediaPage": "HasSocialNet",
    "HasSubmitButton": "HasSubmitButton",
    "HasCopyrightInfoKey": "HasCopyrightInfo",
    "CntImages": "NoOfImage",
    "CntFilesJS": "NoOfJS",
    "CntSelfHRef": "NoOfSelfRef",
    "CntEmptyRef": "NoOfEmptyRef",
    "CntExternalRef": "NoOfExternalRef",
    "Label": "IsLegit",
}

PREPROCESSOR_FILL_COLS = [
    "CharContinuationRate",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "URLTitleMatchScore",
]

BINARY_COLS = ["Robots", "NoOfiFrame"]

LABEL_MAP = {
    "legitimate": 1,
    "phishing": 0,
    "benign": 1,
    "malicious": 0,
    "ham": 1,
    "spam": 0,
    "1": 1,
    "0": 0,
    "-1": 0,
}


def normalize_label(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        unique_vals = set(series.dropna().unique())
        if unique_vals <= {0, 1}:
            return series.astype(int)
        if unique_vals <= {-1, 1}:
            return series.map({1: 1, -1: 0})

    labels = series.astype(str).str.strip().str.lower()
    mapped = labels.map(LABEL_MAP)
    unknown = sorted(set(labels[mapped.isna()].unique()))
    if unknown:
        raise ValueError(
            "Unknown label values in StealthPhisher2025: " + ", ".join(unknown)
        )
    return mapped.astype(int)


def normalize_binary(series: pd.Series, name: str) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return series.fillna(0).astype(int)

    values = series.astype(str).str.strip().str.lower()
    mapping = {
        "1": 1,
        "0": 0,
        "true": 1,
        "false": 0,
        "yes": 1,
        "no": 0,
    }
    mapped = values.map(mapping)
    unknown = sorted(set(values[mapped.isna()].unique()))
    if unknown:
        raise ValueError(
            f"Unknown binary values in StealthPhisher2025 for {name}: "
            + ", ".join(unknown)
        )
    return mapped.astype(int)


def fill_with_preprocessor(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    if not columns:
        return df

    for col in columns:
        if col not in df.columns:
            df[col] = pd.NA

    cache: dict[str, dict] = {}
    feature_methods = {
        "CharContinuationRate": "CharContinuationRate",
        "HasObfuscation": "has_obfuscation",
        "NoOfObfuscatedChar": "no_of_obfuscated_char",
        "ObfuscationRatio": "obfuscation_ratio",
        "URLTitleMatchScore": "URLTitleMatchScore",
    }
    for idx, url in df["URL"].items():
        missing = [col for col in columns if pd.isna(df.at[idx, col])]
        if not missing:
            continue

        if url in cache:
            data = cache[url]
        else:
            extractor = preprocess_data(str(url))
            data: dict[str, float] = {}
            for col, method_name in feature_methods.items():
                try:
                    method = getattr(extractor, method_name)
                    data[col] = method(str(url))
                except Exception:
                    data[col] = 0
            cache[url] = data

        for col in missing:
            if col in data:
                df.at[idx, col] = data[col]

    return df


def main() -> None:
    stealth_df = pd.read_csv(STEALTH_PATH)
    stealth_df.columns = [col.strip() for col in stealth_df.columns]

    required_cols = sorted(STEALTH_TO_UCI.keys())
    missing_cols = [col for col in required_cols if col not in stealth_df.columns]
    if missing_cols:
        raise ValueError(
            "Missing expected columns in StealthPhisher2025: " + ", ".join(missing_cols)
        )

    stealth_df = stealth_df.rename(columns=STEALTH_TO_UCI)
    stealth_df["IsLegit"] = normalize_label(stealth_df["IsLegit"])
    for col in BINARY_COLS:
        if col in stealth_df.columns:
            stealth_df[col] = normalize_binary(stealth_df[col], col)

    target_cols = list(STEALTH_TO_UCI.values())
    stealth_aligned = pd.DataFrame(columns=target_cols)
    for col in target_cols:
        if col in stealth_df.columns:
            stealth_aligned[col] = stealth_df[col]

    stealth_aligned = fill_with_preprocessor(stealth_aligned, PREPROCESSOR_FILL_COLS)

    output_dir = os.path.dirname(OUTPUT_PATH)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    stealth_aligned.to_csv(OUTPUT_PATH, index=False)

    unused_stealth_cols = [
        col for col in stealth_df.columns if col not in target_cols and col != "IsLegit"
    ]
    if unused_stealth_cols:
        print("Stealth columns not used:")
        print(", ".join(sorted(unused_stealth_cols)))

    print(f"Converted dataset saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
