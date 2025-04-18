# utils/dados_reais_loader.py
import pandas as pd

def carregar_dados_esa():
    caminho = "data/ESA-Mission1/arquivo.csv"
    df = pd.read_csv(caminho)
    return df
