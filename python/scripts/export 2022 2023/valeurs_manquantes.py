import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

df = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2023.xlsx", index_col=False, keep_default_na=True, sheet_name='EXPORT', header=4)

def visualiser_valeurs_mq(df):
    val_manq = df.isnull().sum()
    tableau_val_manq = pd.DataFrame({'Valeurs Manquantes': val_manq})
    print(tableau_val_manq.to_string())




