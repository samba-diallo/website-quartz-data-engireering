import json

with open("DE2_Project_Notebook_EN.ipynb", "r") as f:
    nb = json.load(f)

c24_source = """# 3.5 Comparaison empreinte Parquet vs CSV
import pathlib
import os

# Sauvegarder aussi en CSV pour comparer (CSV ne supporte pas les arrays, on les convertit en string)
csv_path = CFG["paths"]["text"] + "_csv"
inverted_index.withColumn("doc_ids", F.concat_ws(",", "doc_ids")).write.mode("overwrite").option("header", "true").csv(csv_path)

def get_size(path):
    return sum(f.stat().st_size for f in pathlib.Path(path).glob('**/*') if f.is_file())

size_parquet = get_size(CFG["paths"]["text"])
size_csv = get_size(csv_path)
ratio = (size_parquet / size_csv) * 100 if size_csv > 0 else 0

record_metric("Text", "storage_ratio_pct", ratio, "Parquet vs CSV")
print(f"Taille CSV     : {size_csv / 1024 / 1024:.2f} MB")
print(f"Taille Parquet : {size_parquet / 1024 / 1024:.2f} MB")
print(f"Ratio Parquet/CSV : {ratio:.1f}% (SLO <= 60%)")"""

nb["cells"][24]["source"] = [line + "\n" for line in c24_source.split("\n")]
if nb["cells"][24]["source"][-1].endswith("\n\n"):
    nb["cells"][24]["source"][-1] = nb["cells"][24]["source"][-1][:-1]

with open("DE2_Project_Notebook_EN.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook CSV fixed!")
