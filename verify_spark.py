# Option A: pip-installed PySpark verification script
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('DE2-verify').getOrCreate()
print('Spark version:', spark.version)

df = spark.range(10)
df.explain('formatted')

spark.stop()
