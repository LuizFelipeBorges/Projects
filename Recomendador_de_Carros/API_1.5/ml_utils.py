import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json

mdl_rf = jb.load("random_forest_20082020.pkl.z")
mdl_lgbm = jb.load("lgbm_20082020.pkl.z")
vectorizer_ano = jb.load("vectorizer_ano_20082020.pkl.z")
vectorizer_modelo = jb.load("vectorizer_modelo_20082020.pkl.z")

def clean_valor(data):

    valor = (data["valor"])

    if valor == "Consulte-nos":
        valor = 0
    else:
        valor = valor.replace("R$", "")
        valor = valor.replace(",", "")
        valor = pd.to_numeric(valor)
        valor = valor*1000
        
    return valor


def clean_km(data):

    km = data["km"]

    if (km == "Gasolina") or (km == "Flex"):
        km = 0
    else:
        km = pd.to_numeric(km)
        km = km*1000

    return km


def compute_features(data):

    modelo = data["modelo"].replace("-", " ")
    valor = clean_valor(data)
    km = clean_km(data)
    ano = data["ano"]

    features = dict()

    features["km"] = km
    features["valor"] = valor
    
    vec_modelo = vectorizer_modelo.transform([modelo])
    vec_ano = vectorizer_ano.transform([ano])

    num_features = csr_matrix(np.array([features["valor"], features["km"]]))
    feature_array = hstack([num_features, vec_modelo, vec_ano])

    return feature_array


def compute_prediction(data):
    feature_array = compute_features(data)

    #p_lgbm = mdl_lgbm.predict_proba(feature_array)[0][1]
    p_rf = mdl_rf.predict_proba(feature_array)[0][1]

    #p = 0.5*p_rf + 0.5*p_lgbm

    return p_rf







