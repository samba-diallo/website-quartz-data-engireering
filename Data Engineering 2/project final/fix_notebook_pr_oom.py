import json

with open("DE2_Project_Notebook_EN.ipynb", "r") as f:
    nb = json.load(f)

c27_source = """# 4.2 PageRank Itératif
t0_pr = time.time()
MAX_ITER = CFG.get("pagerank", {}).get("max_iter", 10)
DAMPING = CFG.get("pagerank", {}).get("damping", 0.85)

# Configurer un répertoire de checkpoint pour couper le lineage
import tempfile
spark.sparkContext.setCheckpointDir(tempfile.gettempdir() + "/spark_checkpoint")

# Nœuds uniques (acteurs et dépôts combinés)
vertices = edges.select("src").union(edges.select(F.col("dst").alias("src"))).distinct().localCheckpoint()
N = vertices.count()

# Initialisation : chaque nœud commence avec un rang de 1/N
ranks = vertices.withColumn("rank", F.lit(1.0 / N)).localCheckpoint()

for i in range(MAX_ITER):
    # Calculer les contributions : rank_source / out_degree_source
    contribs = edges.join(ranks, "src") \\
        .join(out_degree, "src") \\
        .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
    
    # Mettre à jour les rangs : (1 - d)/N + d * sum(contributions) pour TOUS les noeuds
    sum_contribs = contribs.groupBy("src").agg(F.sum("contrib").alias("sum_contrib"))
    
    new_ranks = vertices.join(sum_contribs, "src", "left_outer") \\
        .select("src", (F.lit(1 - DAMPING) / N + DAMPING * F.coalesce(F.col("sum_contrib"), F.lit(0.0))).alias("rank"))
    
    # IMPORTANT: Utiliser localCheckpoint() pour couper le lineage exponentiel (évite OOM)
    new_ranks = new_ranks.localCheckpoint()
    
    # Calculer la convergence (différence absolue totale)
    delta = ranks.join(new_ranks, "src", "full_outer") \\
        .select(F.abs(F.coalesce(ranks["rank"], F.lit(0)) - F.coalesce(new_ranks["rank"], F.lit(0))).alias("diff")) \\
        .agg(F.sum("diff")).collect()[0][0]
    
    delta_val = delta if delta is not None else 0.0
    record_metric("Iterative", f"pagerank_delta", delta_val, f"Iteration {i+1}")
    print(f"Itération {i+1} - Delta : {delta_val:.6f}")
    
    ranks = new_ranks

# Sauvegarder les résultats
pr_output = os.path.join(CFG["paths"]["gold"], "pagerank")
ranks.orderBy(F.desc("rank")).write.mode("overwrite").parquet(pr_output)

t1_pr = time.time()
record_metric("Iterative", "pagerank_latency_sec", t1_pr - t0_pr, f"{MAX_ITER} itérations")
print(f"PageRank terminé en {t1_pr - t0_pr:.2f} secondes. Top 10 influents :")
ranks.orderBy(F.desc("rank")).show(10, truncate=False)"""

nb["cells"][27]["source"] = [line + "\n" for line in c27_source.split("\n")]
if nb["cells"][27]["source"][-1].endswith("\n\n"):
    nb["cells"][27]["source"][-1] = nb["cells"][27]["source"][-1][:-1]


with open("DE2_Project_Notebook_EN.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook PR OOM fixed!")
