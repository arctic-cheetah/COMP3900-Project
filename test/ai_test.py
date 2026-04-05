import pandas
import backend.preprocessor as p


def test_preprocessor():
    # https://www.southbankmosaics.com
    URL = "https://www.southbankmosaics.com"
    preprocessor = p.preprocess_data(URL)
    url_features: pandas.DataFrame = preprocessor.get_data()
    out = url_features.to_string(
        header=False, index=False, float_format="{:.3f}".format
    )
    print(out)
    # TODO: Make this test more extensible by allowing more feature var columns to be added
    EXPECTED_OUT = "32 24 0 1.000 3 1 0 0 0.000 18 0.581 0 0.000 0 0 0 1 0.032 1 560 9462 1 38 1 191 12 7"
    assert out == EXPECTED_OUT
    print("Url features as predicted")

    pass
