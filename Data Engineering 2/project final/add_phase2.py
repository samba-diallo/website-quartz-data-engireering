"""
Ajoute les cellules de la Phase 2 (Streaming) au notebook.
"""
import json

with open("DE2_Project_Notebook_EN.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

phase2_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Phase 2 : Ingestion Streaming (Structured Streaming)\n",
            "\n",
            "Cette phase implémente l'ingestion en continu via **Structured Streaming** avec une **source fichier**.\n",
            "Le script `simulate_streaming.py` dépose les fichiers `.json.gz` un par un dans `data/landing/`.\n",
            "Spark les détecte automatiquement et les traite comme des micro-batches.\n",
            "\n",
            "**Composants clés :**\n",
            "- `readStream` avec `maxFilesPerTrigger=1` (1 fichier par micro-batch)\n",
            "- Agrégation fenêtrée avec **watermark** (retard toléré de 10 min)\n",
            "- Fenêtre temporelle de 5 minutes\n",
            "- Écriture en mode **append** vers Parquet\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2.1 Schéma de lecture pour le streaming\n",
            "En streaming, Spark ne peut pas inférer le schéma automatiquement.\n",
            "On définit donc un schéma explicite basé sur les champs principaux de GitHub Archive."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 2.1 Schéma explicite pour le streaming\n",
            "# En mode streaming, Spark ne peut pas inférer le schéma à la volée.\n",
            "# On le définit manuellement à partir des champs GitHub Archive.\n",
            "from pyspark.sql.types import StructType, StructField, StringType, LongType\n",
            "\n",
            "streaming_schema = StructType([\n",
            "    StructField(\"id\", StringType(), True),\n",
            "    StructField(\"type\", StringType(), True),\n",
            "    StructField(\"actor\", StructType([\n",
            "        StructField(\"login\", StringType(), True),\n",
            "    ]), True),\n",
            "    StructField(\"repo\", StructType([\n",
            "        StructField(\"name\", StringType(), True),\n",
            "    ]), True),\n",
            "    StructField(\"created_at\", StringType(), True),\n",
            "])\n",
            "\n",
            "print(\"Schéma de streaming défini.\")\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2.2 Lancement du flux Structured Streaming\n",
            "On lit les fichiers JSON déposés dans `data/landing/` avec `readStream`.\n",
            "On applique une **agrégation fenêtrée** avec un **watermark**.\n",
            "\n",
            "**IMPORTANT :** Avant d'exécuter cette cellule, lancez `simulate_streaming.py` dans un terminal séparé :\n",
            "```bash\n",
            "python simulate_streaming.py\n",
            "```"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 2.2 Démarrer le flux Structured Streaming\n",
            "import shutil\n",
            "\n",
            "# Nettoyer les sorties précédentes pour repartir de zéro\n",
            "for d in [CFG[\"paths\"][\"streaming\"], CFG[\"paths\"][\"streaming_checkpoint\"]]:\n",
            "    if os.path.exists(d):\n",
            "        shutil.rmtree(d)\n",
            "\n",
            "# Lire le flux depuis le dossier landing/ (source fichier)\n",
            "# maxFilesPerTrigger=1 : on ne traite qu'un fichier par micro-batch\n",
            "stream_df = spark.readStream \\\n",
            "    .schema(streaming_schema) \\\n",
            "    .option(\"maxFilesPerTrigger\", 1) \\\n",
            "    .json(CFG[\"paths\"][\"streaming_landing\"])\n",
            "\n",
            "# Convertir created_at en timestamp pour le watermark\n",
            "stream_typed = stream_df \\\n",
            "    .withColumn(\"event_ts\", F.to_timestamp(F.col(\"created_at\"))) \\\n",
            "    .filter(F.col(\"event_ts\").isNotNull())\n",
            "\n",
            "# Agrégation fenêtrée avec watermark :\n",
            "# - Watermark : on tolère un retard avant de fermer une fenêtre\n",
            "# - Fenêtre temporelle : on agrège les événements par tranches\n",
            "windowed_counts = stream_typed \\\n",
            "    .withWatermark(\"event_ts\", CFG[\"streaming\"][\"watermark\"]) \\\n",
            "    .groupBy(\n",
            "        F.window(\"event_ts\", CFG[\"streaming\"][\"window_duration\"]),\n",
            "        F.col(\"type\").alias(\"event_type\")\n",
            "    ) \\\n",
            "    .agg(F.count(\"*\").alias(\"event_count\"))\n",
            "\n",
            "# Écriture en mode append vers Parquet avec checkpoint\n",
            "streaming_query = windowed_counts.writeStream \\\n",
            "    .outputMode(\"append\") \\\n",
            "    .format(\"parquet\") \\\n",
            "    .option(\"path\", CFG[\"paths\"][\"streaming\"]) \\\n",
            "    .option(\"checkpointLocation\", CFG[\"paths\"][\"streaming_checkpoint\"]) \\\n",
            "    .trigger(processingTime=CFG[\"streaming\"][\"trigger_interval\"]) \\\n",
            "    .start()\n",
            "\n",
            "wm = CFG['streaming']['watermark']\n",
            "ti = CFG['streaming']['trigger_interval']\n",
            "wd = CFG['streaming']['window_duration']\n",
            "print(\"Streaming démarré. En attente des fichiers dans data/landing/ ...\")\n",
            "print(f\"Trigger : {ti}  |  Watermark : {wm}  |  Fenêtre : {wd}\")\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2.3 Surveillance du flux et capture des métriques\n",
            "On attend que le flux traite tous les fichiers disponibles, puis on capture `query.lastProgress`\n",
            "comme preuve du bon fonctionnement du streaming."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 2.3 Attendre le traitement et capturer les preuves\n",
            "import json as json_lib\n",
            "\n",
            "# Attendre que le streaming traite les fichiers disponibles\n",
            "WAIT_SECONDS = 90\n",
            "print(f\"Attente de {WAIT_SECONDS}s pour laisser le streaming traiter les fichiers...\")\n",
            "time.sleep(WAIT_SECONDS)\n",
            "\n",
            "# Capturer query.lastProgress comme preuve\n",
            "last_progress = streaming_query.lastProgress\n",
            "if last_progress:\n",
            "    print(\"=== query.lastProgress ===\")\n",
            "    print(json_lib.dumps(last_progress, indent=2))\n",
            "    \n",
            "    # Sauvegarder la preuve dans proof/\n",
            "    os.makedirs(CFG[\"paths\"][\"proof\"], exist_ok=True)\n",
            "    proof_path = os.path.join(CFG[\"paths\"][\"proof\"], \"streaming_lastProgress.json\")\n",
            "    with open(proof_path, \"w\", encoding=\"utf-8\") as f:\n",
            "        json_lib.dump(last_progress, f, indent=2)\n",
            "    print(f\"Preuve sauvegardée : {proof_path}\")\n",
            "    \n",
            "    # Enregistrer la métrique\n",
            "    record_metric(\"Streaming\", \"streaming_trigger_latency\",\n",
            "                  last_progress.get(\"batchDuration\", \"N/A\"),\n",
            "                  f\"Batch {last_progress.get('batchId', 'N/A')}\")\n",
            "else:\n",
            "    print(\"Aucun batch traité. Vérifiez que simulate_streaming.py a déposé des fichiers.\")\n",
            "\n",
            "# Arrêter proprement le flux\n",
            "streaming_query.stop()\n",
            "print(\"Streaming arrêté proprement.\")\n",
            "\n",
            "# Vérifier les résultats écrits\n",
            "result_df = spark.read.parquet(CFG[\"paths\"][\"streaming\"])\n",
            "print(f\"\\nNombre de lignes dans la sortie streaming : {result_df.count()}\")\n",
            "result_df.orderBy(\"window\").show(10, truncate=False)\n"
        ]
    },
]

nb["cells"].extend(phase2_cells)

with open("DE2_Project_Notebook_EN.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Phase 2 ajoutée : {len(phase2_cells)} cellules insérées dans le notebook.")
