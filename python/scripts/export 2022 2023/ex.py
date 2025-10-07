import pandas as pd

df = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\export 2023.xls" ,index_col=False, keep_default_na=True, sheet_name='Sheet1', header=0)

df.to_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\export 2023.xlsx", index=False)