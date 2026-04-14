from Levenshtein import distance, jaro_winkler
from pylcs import lcs_sequence_length
import pandas as pd

whitelist_path: str = "backend/ml/data/top_100k_domains.csv"
model_path: str = "backend/ml/models/logit_model.pkl"


#  Where 1 is identical and 0 is different.
def normalised_levenshtein(a: str, b: str):
    return 1 - distance(a, b) / max(len(a), len(b))


#  Where 1 is identical and 0 is different.
def normalised_lcs(a: str, b: str):
    return (2 * lcs_sequence_length(a, b)) / (len(a) + len(b))


def get_whitelist(whitelist_filepath: str):
    whitelist_df = pd.read_csv(whitelist_filepath)
    return whitelist_df["Domain"].tolist()


# helper make domain consistent
def _normalize_domain(url: str):
    url = url.strip().lower().strip(".")
    if url.startswith("www."):
        url = url[4:]
    return url


# helper func to check for subdomain from whitelist
def _is_domain_or_subdomain(domain: str, whitelist_domain: str):
    if domain == whitelist_domain:
        return True
    return domain.endswith("." + whitelist_domain)


def search_whitelist(domain: str, whitelist: list[str]):
    domain = _normalize_domain(domain)
    whitelist_set = {_normalize_domain(w) for w in whitelist}
    # We need to normalise the domain
    # search for whitelist subdomain here!
    # make a set of whitelist subdomain
    for whitelist_domain in whitelist_set:
        if _is_domain_or_subdomain(domain, whitelist_domain):
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
