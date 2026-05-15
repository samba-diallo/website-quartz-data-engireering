import json

with open("DE2_Project_Notebook_EN.ipynb", "r") as f:
    nb = json.load(f)

c27_source = """# 4.2 PageRank Itératif
t0_pr = time.time()
MAX_ITER = CFG.get("pagerank", {}).get("max_iter", 10)
DAMPING = CFG.get("pagerank", {}).get("damping", 0.85)

# Nœuds uniques (acteurs et dépôts combinés)
vertices = edges.select("src").union(edges.select(F.col("dst").alias("src"))).distinct().cache()
N = vertices.count()

# Initialisation : chaque nœud commence avec un rang de 1/N
ranks = vertices.withColumn("rank", F.lit(1.0 / N))

for i in range(MAX_ITER):
    # Calculer les contributions : rank_source / out_degree_source
    contribs = edges.join(ranks, "src") \\
        .join(out_degree, "src") \\
        .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
    
    # Mettre à jour les rangs : (1 - d)/N + d * sum(contributions) pour TOUS les noeuds
    sum_contribs = contribs.groupBy("src").agg(F.sum("contrib").alias("sum_contrib"))
    
    new_ranks = vertices.join(sum_contribs, "src", "left_outer") \\
        .select("src", (F.lit(1 - DAMPING) / N + DAMPING * F.coalesce(F.col("sum_contrib"), F.lit(0.0))).alias("rank")).cache()
    
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


c28_source = """# 4.3 Expérience de partitionnement
# Test de la configuration "optimisée" en repartitionnant par hachage
t0_opt = time.time()
edges_opt = edges.repartition(CFG["spark"]["partitions"], "src").cache()
out_degree_opt = edges_opt.groupBy("src").count().withColumnRenamed("count", "out_deg").cache()

ranks_opt = vertices.withColumn("rank", F.lit(1.0 / N))

for i in range(2): # Juste 2 itérations pour le test de temps
    contribs = edges_opt.join(ranks_opt, "src") \\
        .join(out_degree_opt, "src") \\
        .select(F.col("dst").alias("src"), (F.col("rank") / F.col("out_deg")).alias("contrib"))
    
    sum_contribs = contribs.groupBy("src").agg(F.sum("contrib").alias("sum_contrib"))
    ranks_opt = vertices.join(sum_contribs, "src", "left_outer") \\
        .select("src", (F.lit(1 - DAMPING) / N + DAMPING * F.coalesce(F.col("sum_contrib"), F.lit(0.0))).alias("rank")).cache()
    ranks_opt.count() # Force execution

t1_opt = time.time()
record_metric("Iterative", "pagerank_opt_latency_sec", t1_opt - t0_opt, "2 itérations optimisées")
print(f"Temps avec partitionnement optimisé (2 iters) : {t1_opt - t0_opt:.2f}s")"""

nb["cells"][28]["source"] = [line + "\n" for line in c28_source.split("\n")]
if nb["cells"][28]["source"][-1].endswith("\n\n"):
    nb["cells"][28]["source"][-1] = nb["cells"][28]["source"][-1][:-1]

with open("DE2_Project_Notebook_EN.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook PR fixed!")
