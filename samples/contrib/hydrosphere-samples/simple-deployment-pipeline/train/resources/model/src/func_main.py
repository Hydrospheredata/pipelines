import pandas as pd
import logging
from joblib import load


clf = load('/model/files/classification_model.joblib')
ordinal_encoder = load('/model/files/column_transformer.joblib')

CATEGORICAL_FEATURES = [
    "workclass", "education", "marital_status", "occupation", "relationship", "race", "sex", 
    "capital_gain", "capital_loss", "country"
]

def predict(**kwargs):
    X = pd.DataFrame.from_dict({0: kwargs}).T
    cat_X = ordinal_encoder.transform(X[CATEGORICAL_FEATURES])
    cat_X = pd.DataFrame(cat_X, columns=CATEGORICAL_FEATURES)
    processed_X = cat_X.join(X[set(X.columns) - set(CATEGORICAL_FEATURES)])
    predicted = clf.predict(processed_X)
    return {"income": predicted.astype(int)[0]}
