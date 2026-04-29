import pandas
import backend.ml.preprocessor as p


def test_preprocessor():
    # https://www.southbankmosaics.com
    URL = [
        "https://www.southbankmosaics.com",
        # "https://www.uni-mainz.de",
        # "https://www.voicefmradio.co.uk",
    ]

    out = get_output_preprocessor(URL[0])
    # TODO: Make this test more extensible by allowing more feature var columns to be added
    # Also remove websites where the feature variables for JS code change due to dependencies
    EXPECTED_OUT = [
        "32 24 0 1.000 3 1 0 0 0.000 18 0.581 0 0.000 0 0 0 1 0.032 1 1120 946 1 0.000 1 1 0 1 1 1 197 14 8",
        # "24 16 0 0.667 2 1 0 0 0.000 9 0.391 0 0.000 0 0 0 2 0.087 1 2324 11400 1 55.556 1 1 1 1 1 0 66 54 82",
        # "30 22 0 0.867 5 1 0 0 0.000 15 0.517 0 0.000 0 0 0 1 0.034 1 1067 2052 1 46.667 0 1 1 1 1 0 68 8 60",
    ]

    for idx, url in enumerate(URL):
        out = get_output_preprocessor(url)
        assert EXPECTED_OUT[idx] == out
        print(f"URL :{idx} feature variable output matches for: {url}")

    pass


def get_output_preprocessor(URL):
    preprocessor = p.preprocess_data(URL)
    url_features: pandas.DataFrame = preprocessor.get_data().iloc[:, 1:]
    out = url_features.to_string(
        header=False, index=False, float_format="{:.3f}".format
    )
    print(out)
    return out
