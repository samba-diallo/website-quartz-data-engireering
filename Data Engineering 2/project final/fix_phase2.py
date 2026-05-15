"""
Corrige la cellule 2.3 du notebook pour gérer les UUID dans lastProgress.
"""
import json

with open("DE2_Project_Notebook_EN.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

# Trouver la cellule qui contient "query.lastProgress" et la corriger
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        src = "".join(cell["source"])
        if "query.lastProgress" in src and "json_lib.dumps" in src:
            cell["source"] = [
                "# 2.3 Attendre le traitement et capturer les preuves\n",
                "import json as json_lib\n",
                "from uuid import UUID\n",
                "\n",
                "# Encodeur personnalisé pour gérer les UUID dans lastProgress\n",
                "class SafeEncoder(json_lib.JSONEncoder):\n",
                "    def default(self, obj):\n",
                "        if isinstance(obj, UUID):\n",
                "            return str(obj)\n",
                "        return super().default(obj)\n",
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
                "    print(json_lib.dumps(last_progress, indent=2, cls=SafeEncoder))\n",
                "    \n",
                "    # Sauvegarder la preuve dans proof/\n",
                "    os.makedirs(CFG[\"paths\"][\"proof\"], exist_ok=True)\n",
                "    proof_path = os.path.join(CFG[\"paths\"][\"proof\"], \"streaming_lastProgress.json\")\n",
                "    with open(proof_path, \"w\", encoding=\"utf-8\") as f:\n",
                "        json_lib.dump(last_progress, f, indent=2, cls=SafeEncoder)\n",
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
                "result_df.orderBy(\"window\").show(10, truncate=False)\n",
            ]
            print("Cellule 2.3 corrigée.")
            break

with open("DE2_Project_Notebook_EN.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print("Notebook sauvegardé.")
