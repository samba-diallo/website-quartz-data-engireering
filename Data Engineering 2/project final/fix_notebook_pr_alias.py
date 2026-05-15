import json

with open("DE2_Project_Notebook_EN.ipynb", "r") as f:
    nb = json.load(f)

c27_source = "".join(nb["cells"][27]["source"])
c27_source = c27_source.replace(
    'delta = ranks.join(new_ranks, "src", "full_outer") \\\n        .select(F.abs(F.coalesce(ranks["rank"], F.lit(0)) - F.coalesce(new_ranks["rank"], F.lit(0))).alias("diff"))',
    'delta = ranks.alias("old").join(new_ranks.alias("new"), "src", "full_outer") \\\n        .select(F.abs(F.coalesce(F.col("old.rank"), F.lit(0)) - F.coalesce(F.col("new.rank"), F.lit(0))).alias("diff"))'
)

nb["cells"][27]["source"] = [line + "\n" for line in c27_source.split("\n")]
if nb["cells"][27]["source"][-1].endswith("\n\n"):
    nb["cells"][27]["source"][-1] = nb["cells"][27]["source"][-1][:-1]

with open("DE2_Project_Notebook_EN.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook PR alias fixed!")
