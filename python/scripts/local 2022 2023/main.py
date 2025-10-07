import pandas as pd
from valeurs_manquantes import visualiser_valeurs_mq,remplir
from valeurs_aberrantes import visualiser_valeurs_aberrantes
from transformation import mapping
import re
def main():
    # Charger les données
    print("Chargement des données...")
    df = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2023.xlsx", engine="odf", index_col=False, keep_default_na=True, sheet_name='LOCAL', header=4)
    df2 = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2022.xlsx", engine="odf", index_col=False, keep_default_na=True, sheet_name='LOCAL', header=4)
    df.columns = df.columns.str.strip()  # Supprime espaces début/fin des noms de colonnes
    df2.columns = df2.columns.str.strip()  # Supprime espaces début/fin des noms de colonnes
    # Étape 1: Analyse et traitement des valeurs manquantes
    print("\n=== ANALYSE DES VALEURS MANQUANTES ===")
    visualiser_valeurs_mq(df)
    visualiser_valeurs_mq(df2)
    print("\n=== TRAITEMENT DES VALEURS MANQUANTES ===")
    df = remplir(df)
    df["RESTANT"]= df["RESTANT"].fillna(0)
    df2 = remplir(df2)
    df2["RESTANT"]= df2["RESTANT"].fillna(0)

    def nettoyer_departement(val):
        if isinstance(val, str):
        # Supprimer doublons consécutifs (ex: "ELECTRICITE ELECTRICITE" -> "ELECTRICITE")
            return re.sub(r'\b(\w+)\s+\1\b', r'\1', val, flags=re.IGNORECASE)
        return val

    df["departement"] = df["departement"].apply(nettoyer_departement)
    df2["departement"] = df2["departement"].apply(nettoyer_departement)

    df['departement']= df['departement'].replace({
        'GENI CIVIL' : 'Génie Civil',
        'ELECTRICITE': 'Electricité',
        'FLUIDE': 'Fluide',
        'ELECTRICITEELECTRICITE': 'Electricité',
    })
    df2['departement']= df2['departement'].replace({
        'GENI CIVIL' : 'Génie Civil',
        'ELECTRICITE': 'Electricité',
        'FLUIDE': 'Fluide',
        'ELECTRICITEELECTRICITE': 'Electricité',
    })
    # Étape 3: Analyse des valeurs aberrantes
    print("\n=== ANALYSE DES VALEURS ABERRANTES ===")
    colonnes_numeriques = ['N° FCT','HT','tva 19%','TTC','RECOUVREMENT','RESTANT']
    visualiser_valeurs_aberrantes(df, colonnes_numeriques)
    
    # Étape 4: Transformation des données
    print("\n=== TRANSFORMATION DES DONNÉES ===")
    df = mapping(df)
    df2 = mapping(df2)
    print("Mapping des départements appliqué.")

    # Etape 5: date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
    df2['Date'] = pd.to_datetime(df2['Date'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
    # Étape 5: Export des données nettoyées
    print("\n=== EXPORT DES DONNÉES NETTOYÉES ===")
    output_path = "C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\local 2023.xlsx"
    df.to_excel(output_path, index=False)
    df2.to_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\local 2022.xlsx", index=False)

if __name__ == "__main__":
    main()