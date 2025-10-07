import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.ensemble import IsolationForest


#fonction pour visualiser les valeurs aberrantes avec boxplot
def visualiser_valeurs_aberrantes(df, colonnes):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df[colonnes])
    plt.title("Boxplot des colonnes numériques (EXPORT)")
    plt.xlabel("Variables ")
    plt.show(block=False)
    input("Appuyez sur Entrée pour fermer le graphique...")

#fonction pour détecter les valeurs aberrantes iqr
def detect_outliers_iqr(data, columns):
    outliers_dict = {}
    for col in columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
        if not outliers.empty:  # s'il y a des valeurs aberrantes
            print(f"\n--- Valeurs aberrantes pour {col} ---")
            print(outliers[[col]])
        outliers_dict[col] = outliers

    return outliers_dict

#fonction pour détecter et remplir les valeurs aberrantes iqr
def detect_et_remplir_outliers_iqr(data, columns):
    for col in columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        mediane = data[col].median()
        data[col] = data[col].mask((data[col] < lower_bound) | (data[col] > upper_bound), mediane)
    return data