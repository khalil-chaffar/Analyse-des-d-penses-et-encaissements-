import pandas as pd
# Commenter les imports problématiques
# from valeurs_manquantes import visualiser_valeurs_mq
# from transformation import mapping
import warnings
warnings.filterwarnings('ignore')

def main():
    try:
        # Charger les données avec l'engine ODF (qui fonctionnait)
        print("Chargement des données...")
        df = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2023.xlsx", 
                          engine="odf",  # Retour à ODF qui fonctionnait
                          index_col=False, 
                          keep_default_na=True, 
                          sheet_name='SALAIRES', 
                          header=6)
        
        df2 = pd.read_excel("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data\\DATA FORMATION BI 2022.xlsx", 
                           engine="odf",  # Retour à ODF
                           index_col=False, 
                           keep_default_na=True, 
                           sheet_name='SALAIRES', 
                           header=6)
        
        print(f"Données 2023 chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
        print(f"Données 2022 chargées : {df2.shape[0]} lignes, {df2.shape[1]} colonnes")
        
        # Vérifier les colonnes
        print(f"Colonnes 2023 : {len(df.columns)} colonnes")
        print(f"Colonnes 2022 : {len(df2.columns)} colonnes")
        
        # === ANALYSE DES VALEURS MANQUANTES (VERSION MANUELLE) ===
        print("\n=== ANALYSE DES VALEURS MANQUANTES (MANUELLE) ===")
        print("\nValeurs manquantes 2023 :")
        missing_2023 = df.isnull().sum()
        print(missing_2023[missing_2023 > 0])  # Seulement les colonnes avec des NaN
        
        print(f"\nPourcentage de valeurs manquantes 2023 :")
        for col in df.columns:
            pct = (df[col].isnull().sum() / len(df)) * 100
            if pct > 0:
                print(f"  {col}: {pct:.2f}%")
        
        print("\nValeurs manquantes 2022 :")
        missing_2022 = df2.isnull().sum()
        print(missing_2022[missing_2022 > 0])
        
        print(f"\nPourcentage de valeurs manquantes 2022 :")
        for col in df2.columns:
            pct = (df2[col].isnull().sum() / len(df2)) * 100
            if pct > 0:
                print(f"  {col}: {pct:.2f}%")
        
        # Nettoyage des départements
        print("\n=== NETTOYAGE DES DÉPARTEMENTS ===")
        df['DEPARTEMENT'] = df['DEPARTEMENT'].fillna('').astype(str).str.strip().replace({
            'GCIVILE' : 'Génie Civil',
            'ELEC': 'Electricité',
            'FLUIDE': 'Fluide',
        })
        
        df2['DEPARTEMENT'] = df2['DEPARTEMENT'].fillna('').astype(str).str.strip().replace({
            'GCIVILE' : 'Génie Civil',
            'ELEC': 'Electricité',
            'FLUIDE': 'Fluide',
        })
        
        print("Nettoyage départements terminé.")
        
        # === TRANSFORMATION DES DONNÉES ===
        print("\n=== TRANSFORMATION DES DONNÉES ===")
        dep_mapping = {
            'Fluide' : 0,
            'Génie Civil' : 1,
            'Electricité' : 2,
        }
        
        df['dep_code'] = df['DEPARTEMENT'].map(dep_mapping)
        df2['dep_code'] = df2['DEPARTEMENT'].map(dep_mapping)
        print("Mapping des départements appliqué.")
        
        # Transformation des mois
        mois_map = {
            "JANVIER": 1, "FEVRIER": 2, "MARS": 3, "AVRIL": 4, "MAI": 5, "JUIN": 6,
            "JUILLET": 7, "AOUT": 8, "SEPTEMBRE": 9, "OCTOBRE": 10, "NOVEMBRE": 11, "DECEMBRE": 12
        }
        
        # Nettoyage et transformation des mois
        df["MOIS"] = df["MOIS"].fillna('').astype(str).str.strip().str.upper()
        df2["MOIS"] = df2["MOIS"].fillna('').astype(str).str.strip().str.upper()
        
        # Créer les numéros de mois avec gestion d'erreur
        df["MOIS_NUM"] = df["MOIS"].map(mois_map)
        df2["MOIS_NUM"] = df2["MOIS"].map(mois_map)
        
        print(f"Mois non reconnus 2023 : {df['MOIS'][df['MOIS_NUM'].isna()].unique()}")
        print(f"Mois non reconnus 2022 : {df2['MOIS'][df2['MOIS_NUM'].isna()].unique()}")
        
        # === CRÉATION DES DATES AU FORMAT YYYY/MM/DD ===
        print("\n=== CRÉATION DES DATES AU FORMAT YYYY/MM/DD ===")
        
        # Fonction pour créer les dates
        def create_dates(df, year):
            dates = []
            for idx, row in df.iterrows():
                mois_num = row['MOIS_NUM']
                if pd.isna(mois_num) or mois_num < 1 or mois_num > 12:
                    dates.append(None)  # Sera converti en NaT
                else:
                    try:
                        date_obj = pd.to_datetime(f"{year}-{int(mois_num):02d}-01")
                        dates.append(date_obj)
                    except:
                        dates.append(None)
            return pd.Series(dates)
        
        # Créer les dates en format datetime (pour Excel)
        df["Date"] = create_dates(df, 2023)
        df2["Date"] = create_dates(df2, 2022)
        
        # Vérification
        print(f"Nombre de dates valides 2023 : {df['Date'].notna().sum()}")
        print(f"Nombre de dates valides 2022 : {df2['Date'].notna().sum()}")
        
        # === EXPORT DES DONNÉES NETTOYÉES ===
        print("\n=== EXPORT DES DONNÉES NETTOYÉES ===")
        
        # Créer le dossier de sortie
        import os
        os.makedirs("C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees", exist_ok=True)
        
        # Export avec format date pour Excel
        output_path = "C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\salaires_2023.xlsx"
        with pd.ExcelWriter(output_path, engine='openpyxl', date_format='YYYY/MM/DD') as writer:
            df.to_excel(writer, sheet_name='Salaires_2023', index=False)
        
        output_path2 = "C:\\Users\\Administrator\\Desktop\\Projet Bi\\data_traitees\\salaires_2022.xlsx"
        with pd.ExcelWriter(output_path2, engine='openpyxl', date_format='YYYY/MM/DD') as writer:
            df2.to_excel(writer, sheet_name='Salaires_2022', index=False)
        
        print(f"✅ Export terminé : {len(df)} lignes pour 2023, {len(df2)} lignes pour 2022")
        print("✅ Format de date appliqué : YYYY/MM/DD (format date Excel)")
        
        # Statistiques finales
        print("\n=== STATISTIQUES FINALES ===")
        print(f"Total lignes traitées : {len(df) + len(df2)}")
        print(f"Colonnes finales : {list(df.columns)}")
        
    except FileNotFoundError as e:
        print(f"❌ Fichier non trouvé : {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()