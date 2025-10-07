import pandas as pd

df=pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2023.xlsx", index_col=False, keep_default_na=True, sheet_name='EXPORT', header=4)

# Nettoyer la colonne avant mapping
df['departement'] = df['departement'].astype(str).str.strip().str.upper()

def mapping(df):
    dep_mapping = {
        'Fluide' : 0,
        'Génie Civil' : 1,
        'Electricité' : 2,
    }
    df['dep_code'] = df['departement'].map(dep_mapping)
    return df
