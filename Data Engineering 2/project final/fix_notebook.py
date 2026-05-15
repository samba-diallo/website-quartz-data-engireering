import json

with open("DE2_Project_Notebook_EN.ipynb", "r") as f:
    nb = json.load(f)

# Fix Cell 7 (process_silver)
c7_source = "".join(nb["cells"][7]["source"])
c7_source = c7_source.replace(
    'F.to_date(F.col("created_at")).alias("date")',
    'F.to_date(F.col("created_at")).alias("date"),\n            F.col("payload")'
)
nb["cells"][7]["source"] = [line + "\n" for line in c7_source.split("\n")]
if nb["cells"][7]["source"][-1].endswith("\n\n"):
    nb["cells"][7]["source"][-1] = nb["cells"][7]["source"][-1][:-1]

# Fix Cell 20 (Phase 3 text corpus)
c20_source = """# 3.1 Extraction du corpus texte (messages de commit)
t0_text = time.time()
silver_df = spark.read.parquet(CFG["paths"]["silver"])

# Extraire les messages de commit depuis le champ struct 'payload.commits'
corpus = silver_df.filter(F.col("event_type") == "PushEvent") \\
    .withColumn("commit", F.explode("payload.commits")) \\
    .select(
        F.col("commit.sha").alias("doc_id"),
        F.col("commit.message").alias("text")
    ).filter(F.col("text").isNotNull() & (F.length("text") > 0))

print(f"Documents dans le corpus : {corpus.count()}")
corpus.show(5)"""
nb["cells"][20]["source"] = [line + "\n" for line in c20_source.split("\n")]
if nb["cells"][20]["source"][-1].endswith("\n\n"):
    nb["cells"][20]["source"][-1] = nb["cells"][20]["source"][-1][:-1]

# Fix Cell 30 (Phase 5 LLM corpus)
c30_source = """# 5.1 Extraction et curation du dataset LLM
t0_llm = time.time()

# Combiner plusieurs sources de texte pour le dataset LLM
pr_text = silver_df.filter(F.col("event_type") == "PullRequestEvent") \\
    .select(
        F.col("event_id").alias("doc_id"), 
        F.coalesce("payload.pull_request.body", "payload.pull_request.title").alias("text")
    )

llm_corpus = corpus.unionByName(pr_text) # Push messages + PR payloads

min_len = CFG.get("llm", {}).get("min_text_length", 50)

# Filtres qualité : longueur minimale, déduplication exacte (par hash)
df_llm = llm_corpus.filter(F.col("text").isNotNull()) \\
    .filter(F.length("text") >= min_len) \\
    .withColumn("content_hash", F.xxhash64("text")) \\
    .dropDuplicates(["content_hash"]) \\
    .withColumn("source", F.lit("github_archive")) \\
    .withColumn("version", F.lit("v1.0")) \\
    .withColumn("curated_at", F.current_timestamp())

# Sauvegarde
df_llm.write.mode("overwrite").parquet(CFG["paths"]["llm_ready"])

# Mesure de qualité
total_initial = llm_corpus.count()
total_curated = df_llm.count()
pass_rate = (total_curated / total_initial * 100) if total_initial > 0 else 0

record_metric("LLM", "quality_pass_rate_pct", pass_rate, f"Pass rate, min_len={min_len}")
print(f"Documents initiaux : {total_initial}")
print(f"Documents validés  : {total_curated}")
print(f"Taux de passage    : {pass_rate:.1f}% (SLO >= 80%)")"""
nb["cells"][30]["source"] = [line + "\n" for line in c30_source.split("\n")]
if nb["cells"][30]["source"][-1].endswith("\n\n"):
    nb["cells"][30]["source"][-1] = nb["cells"][30]["source"][-1][:-1]

with open("DE2_Project_Notebook_EN.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook fixes applied!")
