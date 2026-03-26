# for x in range(len(train)):
from datetime import time
from typing import List, Tuple

import pandas as pd
from sklearn.base import accuracy_score
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier


# Helper function definiton
from __future__ import annotations

FEATURE_VECTOR = 0
LABEL_VECTOR = 1
POS_LABEL = "IsLegit"

train: List[Tuple[pd.DataFrame, pd.Series]] = []
test: List[Tuple[pd.DataFrame, pd.Series]] = []
SPLIT_RATIO = [(4, 3, 3), (3, 1, 1), (8, 1, 1)]


def evaluate_model(model: "DecisionTreeClassifier", data: Tuple[pd.DataFrame, pd.Series]):
    labels = data[LABEL_VECTOR]
    features = data[FEATURE_VECTOR]
    start = time()
    pred = model.predict(features)
    end = time()
    latency = round((end - start) * 1000, 1)

    accuracy = round(accuracy_score(labels, pred), 3)
    precision = round(precision_score(labels, pred, pos_label=POS_LABEL), 3)
    recall = round(recall_score(labels, pred, pos_label=POS_LABEL), 3)
    # param = f"HyperParameter--> Splitter: , Max_depth: {model.get_depth()}, min_samples_split: {model.get_params()}"
    print(f"Split ratio is: ")
    print(
        f"param: {model} -- Accuracy: {accuracy} / Precision: {precision} / Recall: {recall} / Prediction Latency: {latency}ms"
    )
    conf = confusion_matrix(labels, pred)
    print(conf)

def gridSearchBest(dataSet: int):
    DT_pt2 = DecisionTreeClassifier()
    parameters = {
        "max_depth": [1, 2, 10, 100, 500],
        "max_features": [10, 50, 100, 116],
        "splitter": ["best", "random"],
        "min_samples_split": [2, 10, 20, 50],
    }
    cv = GridSearchCV(DT_pt2, parameters, cv=5, verbose=4)
    cv.fit(train[dataSet][FEATURE_VECTOR], train[dataSet][LABEL_VECTOR])
    print(
        f"Best hyperparameters for {SPLIT_RATIO[dataSet]} ratio are: {cv.best_params_}"
    )
    evaluate_model(cv.best_estimator_, test[0])
    