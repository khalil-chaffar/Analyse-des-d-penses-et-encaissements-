import pandas as pd

df=pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2023.xlsx", index_col=False, keep_default_na=True, sheet_name='SALAIRES', header=6)

# Nettoyer la colonne avant mapping
df['DEPARTEMENT'] = df['DEPARTEMENT'].astype(str).str.strip().str.upper()

def mapping(df):
    dep_mapping = {
    'FLUIDE' : 0,
    'GCIVILE' : 1,
    'ELEC' : 2,
    }

    df['dep_code'] = df['DEPARTEMENT'].map(dep_mapping)
    return df