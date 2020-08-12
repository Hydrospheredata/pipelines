import os
import shutil
import json
from argparse import ArgumentParser

import joblib
import numpy as np
import pandas as pd
import sklearn.ensemble
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, LabelEncoder, OrdinalEncoder


FEATURE_NAMES = [
    "age", "workclass", "fnlwgt", "education", "education-Num", "marital_status", "occupation",
    "relationship", "race", "sex", "capital_gain", "capital_loss", "hours_per_week", "country",
    "income"
]
FEATURES_TO_USE = [
    "age", "workclass", "education", "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "country", "income"
]
CATEGORICAL_FEATURES = [
    "workclass", "education", "marital_status", "occupation", "relationship", "race", "sex", 
    "capital_gain", "capital_loss", "country"
]


# Dictionaries for feature engineering
EDUCATION_MAP = {
    '10th': 'Dropout', '11th': 'Dropout', '12th': 'Dropout', '1st-4th': 'Dropout', '5th-6th': 'Dropout', 
    '7th-8th': 'Dropout', '9th': 'Dropout', 'Preschool': 'Dropout', 'HS-grad': 'High School grad',
    'Some-college': 'High School grad', 'Masters': 'Masters', 'Prof-school': 'Prof-School', 
    'Assoc-acdm': 'Associates', 'Assoc-voc': 'Associates',
}

OCCUPATION_MAP = {
    "Adm-clerical": "Admin", "Armed-Forces": "Military", "Craft-repair": "Blue-Collar", 
    "Exec-managerial": "White-Collar", "Farming-fishing": "Blue-Collar", 
    "Handlers-cleaners": "Blue-Collar", "Machine-op-inspct": "Blue-Collar", 
    "Other-service": "Service", "Priv-house-serv": "Service", "Prof-specialty": "Professional", 
    "Protective-serv": "Other", "Sales": "Sales", "Tech-support": "Other", 
    "Transport-moving": "Blue-Collar",
}

COUNTRY_MAP = {
    'Cambodia': 'SE-Asia', 'Canada': 'British-Commonwealth', 'China': 'China', 
    'Columbia': 'South-America', 'Cuba': 'Other', 'Dominican-Republic': 'Latin-America', 
    'Ecuador': 'South-America', 'El-Salvador': 'South-America', 'England': 'British-Commonwealth',
    'France': 'Euro_1', 'Germany': 'Euro_1', 'Greece': 'Euro_2', 'Guatemala': 'Latin-America', 
    'Haiti': 'Latin-America', 'Holand-Netherlands': 'Euro_1', 'Honduras': 'Latin-America',
    'Hong': 'China', 'Hungary': 'Euro_2', 'India': 'British-Commonwealth', 'Iran': 'Other', 
    'Ireland': 'British-Commonwealth', 'Italy': 'Euro_1', 'Jamaica': 'Latin-America', 
    'Japan': 'Other', 'Laos': 'SE-Asia', 'Mexico': 'Latin-America', 'Nicaragua': 'Latin-America',
    'Outlying-US(Guam-USVI-etc)': 'Latin-America', 'Peru': 'South-America', 'Philippines': 'SE-Asia', 
    'Poland': 'Euro_2', 'Portugal': 'Euro_2', 'Puerto-Rico': 'Latin-America', 
    'Scotland': 'British-Commonwealth', 'South': 'Euro_2', 'Taiwan': 'China', 'Thailand': 'SE-Asia', 
    'Trinadad&Tobago': 'Latin-America', 'United-States': 'United-States', 'Vietnam': 'SE-Asia'
}

MARRIED_MAP = {
    'Never-married': 'Never-Married', 'Married-AF-spouse': 'Married', 'Married-civ-spouse': 'Married', 
    'Married-spouse-absent': 'Separated', 'Separated': 'Separated', 'Divorced': 'Separated', 
    'Widowed': 'Widowed'
}


def cap_gains_fn(x):
    """
    Transform Capita Gain into categories - None, Low, High.
    """
    x = np.array(x.astype(float)).flatten()
    d = np.digitize(x, [0, np.median(x[x > 0]), float('inf')], right=True)
    new_series = np.array(["None"] * len(d))
    new_series[d == 0] = 'None'
    new_series[d == 1] = 'Low'
    new_series[d == 2] = 'High'
    return new_series.reshape(-1, 1)


def map_array_values_fn(value_map):
    """
    Utility function which works like pd.Series.apply(lambda x: map[x]), 
    but adds additional preprocessing.
    """
    def f(series):
        ret = series.str.strip().copy()
        for src, target in value_map.items():
            ret[ret == src] = target
        return np.array(ret).reshape(-1, 1)
    return f


def preprocess(train_path):
    df_raw = pd.read_csv(train_path, header=None, names=FEATURE_NAMES, sep=", ")
    df_raw = df_raw[FEATURES_TO_USE]
    df_raw['income'] = LabelEncoder().fit_transform(df_raw['income'])
    df_raw = df_raw.dropna()

    column_trans = ColumnTransformer([
        ('education_prep', FunctionTransformer(map_array_values_fn(EDUCATION_MAP), validate=False), 'education'),
        ('marital_status_prep', FunctionTransformer(map_array_values_fn(MARRIED_MAP), validate=False), 'marital_status'),
        ('occupation_preprocess', FunctionTransformer(map_array_values_fn(OCCUPATION_MAP), validate=False), 'occupation'),
        ('capital_gain_preprocess', FunctionTransformer(cap_gains_fn, validate=False), ['capital_gain']),
        ('capital_loss_preprocess', FunctionTransformer(cap_gains_fn, validate=False), ['capital_loss']),
        ('country_preproccess', FunctionTransformer(map_array_values_fn(COUNTRY_MAP), validate=False), 'country')
    ], remainder='passthrough')

    df_engineered = pd.DataFrame(
        column_trans.fit_transform(df_raw), 
        columns=[
            'education', 'marital_status', 'occupation', 'capital_gain', 'capital_loss', 'country', 'age', 
            'workclass', 'relationship', 'race', 'sex', 'hours_per_week', 'income'
        ]
    )
    return df_raw, df_engineered


def train(df_raw, df_engineered, random_seed=42):
    X, y = df_engineered.iloc[:, :-1], df_engineered.iloc[:, -1]
    categorical_encoder = OrdinalEncoder()
    encoded_cat_X = categorical_encoder.fit_transform(X[CATEGORICAL_FEATURES])
    encoded_X = pd.DataFrame(encoded_cat_X, columns=CATEGORICAL_FEATURES)
    encoded_X = encoded_X.join(X[set(FEATURES_TO_USE) - {"income"} - set(CATEGORICAL_FEATURES)])

    # Split into train, and put rest aside to split later into val and test
    train_X, rest_X, train_y, rest_y = \
        sklearn.model_selection.train_test_split(encoded_X, y.astype(int), stratify=y, test_size=0.5, random_state=random_seed)
    # Split into validation and test sets
    val_X, test_X, val_y, test_y = \
        sklearn.model_selection.train_test_split(rest_X, rest_y, stratify=rest_y, test_size=0.5, random_state=random_seed)

    clf = sklearn.ensemble.RandomForestClassifier(n_estimators=20, max_depth=10, n_jobs=5, random_state=random_seed)
    clf.fit(train_X, train_y)

    print(f'Train Accuracy: {sklearn.metrics.accuracy_score(train_y, clf.predict(train_X))*100:.2f}%')
    print(f'Validation Accuracy: {sklearn.metrics.accuracy_score(val_y, clf.predict(val_X))*100:.2f}%')
    return clf, categorical_encoder


def main(
        train_path, 
        output_serving_path,
        output_train_path, 
        output_payload_path,
        output_contract_path,
):
    ## Preprocess data and train classifier/transformer
    df_raw, df_engineered = preprocess(train_path)
    clf, tfm = train(df_raw, df_engineered)

    ## Save artifacts for serving
    # Save preprocessed training data for calculating profiles
    os.makedirs(os.path.dirname(output_train_path), exist_ok=True)
    df_engineered.to_csv(output_train_path, index=False)

    ## Prepare serving runtime
    # Save payload for serving
    os.makedirs(os.path.dirname(output_payload_path), exist_ok=True)
    with open(output_payload_path, "w") as file:
        payload = [
            "./src/",
            "./classification_model.joblib",
            "./column_transformer.joblib",
            "./requirements.txt",
        ]
        json.dump(payload, file)

    # Save contract for serving
    os.makedirs(os.path.dirname(output_contract_path), exist_ok=True)
    with open(output_contract_path, "w") as file:
        contract = {
            "signatureName": "predict",  # serving function name
            "inputs": [
                {
                    "name": "age",
                    "shape": "scalar",
                    "type": "int64",
                    "profile": "numerical"
                },
                {
                    "name": "workclass",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "education",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "occupation",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "marital_status",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "relationship",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "race",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "sex",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "capital_gain",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "capital_loss",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
                {
                    "name": "hours_per_week",
                    "shape": "scalar",
                    "type": "int64",
                    "profile": "numerical"
                },
                {
                    "name": "country",
                    "shape": "scalar",
                    "type": "string",
                    "profile": "categorical"
                },
            ],
            "outputs": [
                {
                    "name": "income",
                    "shape": "scalar",
                    "type": "int64",
                    "profile": "categorical",
                }
            ]
        }
        json.dump(contract, file)
    
    # Save model files
    shutil.copytree("model", output_serving_path)
    joblib.dump(clf, os.path.join(output_serving_path, "classification_model.joblib"))
    joblib.dump(tfm, os.path.join(output_serving_path, "column_transformer.joblib"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--train_path", type=str, help="A path to the training data")
    parser.add_argument("--output_serving_path", type=str, help="A path, where to save serving files")
    parser.add_argument("--output_train_path", type=str, help="A path, where to save the preprocessed training data")
    parser.add_argument("--output_payload_path", type=str, help="A path, where to save model's payload")
    parser.add_argument("--output_contract_path", type=str, help="A path, where to save model's contract")
    args = parser.parse_args()

    main(
        args.train_path, 
        args.output_serving_path,
        args.output_train_path,
        args.output_payload_path,
        args.output_contract_path,
    )
