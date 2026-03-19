import os
import pandas as pd

root_folder = "data" 
dataframes = []

for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file.endswith(".txt"):
            filepath = os.path.join(root, file)

            # 1. Extraire le nom du dossier parent (ex: "anas_p1")
            folder_name = os.path.basename(root).lower()
            
            # 2. Séparer le sujet et la phase en gérant les erreurs
            try:
                sujet, phase = folder_name.split('_')
            except ValueError:
                # Si un dossier ne respecte pas le format (ex: dossier caché), on l'ignore
                continue

            # 3. Assigner la classe (y)
            if phase == "p1":
                y = 0  # Calme
            elif phase == "p2":
                y = 1  # Stress
            elif phase == "p3":
                y = 2  # Sport
            else:
                continue

            print(f"Ajout de {sujet} - Phase {phase}...")

            # 4. Lecture propre du fichier Bitalino
            # L'argument comment='#' remplace toute votre boucle de recherche du header !
            # usecols=[5, 6] garantit qu'on prend exactement l'EDA (col 6) et l'ECG (col 7)
            df = pd.read_csv(
                filepath,
                sep='\t',
                comment='#',
                header=None,
                usecols=[5, 6], 
                engine="python"
            )

            # Renommer et nettoyer
            df.columns = ["EDA", "ECG"]
            df = df.apply(pd.to_numeric, errors='coerce').dropna()

            # 5. Ajouter nos métadonnées indispensables
            df["Sujet"] = sujet
            df["y"] = y

            dataframes.append(df)

# 6. Concaténation finale
print("\nAssemblage des fichiers en cours...")
final_df = pd.concat(dataframes, ignore_index=True)
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
final_df.to_csv("dataset_final.csv", index=False)

print(f"CSV créé avec succès : dataset_final.csv")
print(f"Taille totale du dataset : {final_df.shape[0]} lignes de données.")