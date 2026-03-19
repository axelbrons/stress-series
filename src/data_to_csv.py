import os
import pandas as pd

root_folder = "data" 
dataframes = []

for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file.endswith(".txt"):
            filepath = os.path.join(root, file)

            folder_name = os.path.basename(root).lower()
            if folder_name.endswith("p1"):
                y = 0
            elif folder_name.endswith("p2"):
                y = 1
            elif folder_name.endswith("p3"):
                y = 2
            else:
                continue

            with open(filepath, "r") as f:
                lines = f.readlines()

            start_idx = 0
            for i, line in enumerate(lines):
                if "# EndOfHeader" in line:
                    start_idx = i + 1
                    break

            df = pd.read_csv(
                filepath,
                sep=r"\s+",
                skiprows=start_idx,
                header=None,
                engine="python"
            )

            df = df.dropna(axis=1, how='all')

            df = df.iloc[:, -2:]
            df.columns = ["EDA", "ECG"]

            df = df.apply(pd.to_numeric, errors='coerce').dropna()

            df["y"] = y

            dataframes.append(df)

final_df = pd.concat(dataframes, ignore_index=True)
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
final_df.to_csv("dataset_final.csv", index=False)

print("CSV créé : dataset_final.csv")