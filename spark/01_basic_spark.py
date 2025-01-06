from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext

spark = SparkSession.builder \
    .appName("Basic Spark Example") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

    # in some cases below setup to reach the "driver" from "workers" was necessary
    # .config("spark.driver.host", "dev-container") \
    # .config("spark.driver.bindAddress", "0.0.0.0") \

data = [("Alice", 29), ("Bob", 43), ("Cathy", 48)]

columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)

# Data Frame API
df.show()
df_filtered = df.filter(df.Age > 30)
df_filtered.show()

# Spark SQL API
df.createOrReplaceTempView("people")
sql_df = spark.sql("SELECT * FROM people WHERE Age > 30")
sql_df.show()

spark.stop()

# RDD (Resilient Distributed Dataset) API
conf = SparkConf().setAppName("Basic RDD Example").setMaster("spark://spark-master:7077")
sc = SparkContext(conf=conf)

rdd = sc.parallelize(data)
rdd_filtered = rdd.filter(lambda x: x[1] > 30)
print(rdd_filtered.collect())
sc.stop()