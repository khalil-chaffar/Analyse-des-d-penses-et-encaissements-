import pandas as pd
df = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2023.xlsx", index_col=False, keep_default_na=True, sheet_name='EXPORT', header=4)
#print(df.columns)
#print(df.describe())
#print(df.info())
print(df.dtypes)
#print(df.head())