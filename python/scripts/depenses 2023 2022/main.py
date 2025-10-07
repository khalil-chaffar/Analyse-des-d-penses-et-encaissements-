import pandas as pd


def main():
    df = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2023.xlsx",engine="odf", index_col=False, keep_default_na=True, sheet_name='DEPENSES', header=6)
    df2 = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2022.xlsx",engine="odf", index_col=False, keep_default_na=True, sheet_name='DEPENSES', header=6)
    df.columns = df.columns.str.strip()
    df2.columns = df2.columns.str.strip()  # Supprime espaces début/fin des noms de colonnes
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.strftime('%d/%m/%Y')
    df2['DATE'] = pd.to_datetime(df2['DATE'], errors='coerce').dt.strftime('%d/%m/%Y')

    df['DEPARTEMENT']= df['DEPARTEMENT'].replace({
        'GCIVILE' : 'Génie Civil',
        'ELEC': 'Electricité',
        'FLUIDE': 'Fluide',
    })
    df2['DEPARTEMENT']= df2['DEPARTEMENT'].replace({
        'GCIVILE' : 'Génie Civil',
        'ELEC': 'Electricité',
        'FLUIDE': 'Fluide',
    })

    dep_mapping = {
        'Fluide' : 0,
        'Génie Civil' : 1,
        'Electricité' : 2,
    }
    df['dep_code'] = df['DEPARTEMENT'].map(dep_mapping)
    df2['dep_code'] = df2['DEPARTEMENT'].map(dep_mapping)
    path="C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\depenses_2023.xlsx"
    df.to_excel(path, index=False)
    path2="C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\depenses_2022.xlsx"
    df2.to_excel(path2, index=False)

if __name__ == "__main__":
    main()
