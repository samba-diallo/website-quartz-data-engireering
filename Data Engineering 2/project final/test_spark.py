import os
import time
from pyspark.sql import SparkSession

def test_spark_windows():
    print("1. Initialisation de Spark...")
    spark = SparkSession.builder \
        .appName("TestWindows") \
        .master("local[1]") \
        .config("spark.sql.adaptive.enabled", "false") \
        .getOrCreate()
        
    print("2. Création d'un mini DataFrame de 5 lignes...")
    data = [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]
    df = spark.createDataFrame(data, ["lettre", "chiffre"])
    
    print("3. Test d'écriture en Parquet (c'est souvent là que Windows bloque)...")
    t0 = time.time()
    try:
        output_path = "test_windows_parquet"
        df.write.mode("overwrite").parquet(output_path)
        t1 = time.time()
        print(f"✅ SUCCÈS ! L'écriture Parquet a fonctionné en {t1-t0:.2f} secondes.")
    except Exception as e:
        print(f"❌ ERREUR ! Spark n'arrive pas à écrire sur ton disque Windows : {e}")
        
    print("Test terminé.")

if __name__ == "__main__":
    test_spark_windows()
