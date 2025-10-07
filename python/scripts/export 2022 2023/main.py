import pandas as pd
from valeurs_manquantes import visualiser_valeurs_mq
from valeurs_aberrantes import detect_outliers_iqr, visualiser_valeurs_aberrantes
from transformation import mapping
import re

def main():
    # Charger les données
    print("Chargement des données...")
    df = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2023.xlsx", engine="odf" , index_col=False, keep_default_na=True, sheet_name='EXPORT', header=4)
    df2 = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2022.xlsx", engine="odf" , index_col=False, keep_default_na=True, sheet_name='EXPORT', header=4)
    print(f"Dimensions du dataset: {df.shape}")
    
    # Étape 1: Analyse des valeurs manquantes
    print("\n=== ANALYSE DES VALEURS MANQUANTES ===")
    visualiser_valeurs_mq(df)
    visualiser_valeurs_mq(df2)
    
    # Étape 2: Traitement des valeurs manquantes
    print("\n=== TRAITEMENT DES VALEURS MANQUANTES ===")
    df[["Recouvrement €","Restant €"]]= df[["Recouvrement €","Restant €"]].fillna(0)
    df2["Restant €"]= df2["Restant €"].fillna(0)
    
    # Étape 3: Analyse des valeurs aberrantes
    print("\n=== ANALYSE DES VALEURS ABERRANTES ===")
    colonnes_numeriques = ['N° FCT','CA €','tx conv','CA TND','Recouvrement €','Restant €','Perte de change']
    visualiser_valeurs_aberrantes(df, colonnes_numeriques)
    outliers = detect_outliers_iqr(df, colonnes_numeriques)
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
    
    # Étape 4: Transformation des données
    print("\n=== TRANSFORMATION DES DONNÉES ===")
    df = mapping(df)
    df2 = mapping(df2)
    print("Mapping des départements appliqué.")
    # Etape 5: date
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
    df2['DATE'] = pd.to_datetime(df2['DATE'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')

    # Étape 6: Export des données nettoyées
    print("\n=== EXPORT DES DONNÉES NETTOYÉES ===")
    output_path = "C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\export 2023.xlsx"
    df.to_excel(output_path, index=False)
    df2.to_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\export 2022.xlsx", index=False)
    
if __name__ == "__main__":
    main()