from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from pyspark.sql.types import StructType, StructField, IntegerType, MapType, StringType, BooleanType
from pyspark.sql.functions import udf, col


spark = SparkSession.builder \
    .appName("Basic Spark Example") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

    # Below extra classpath was necessary in some cases
    # .config("spark.executor.extraClassPath", "/opt/spark/jars/*") \
    # .config("spark.driver.extraClassPath", "/opt/spark/jars/*") \

data = []
for i in range(1000):
    data.append((i, "source-1", { "category": "category-1", "value": i, "text": f"This is some text {i}"}))

data.append((7001, "source-2", { "category": "category-2", "value": 7001, "text": ""}))

columns = ["id", "source", "data"]
df = spark.createDataFrame(data, columns)
print(f"Count of rows: {df.count()}")
df_filtered = df.filter(df["data.text"] != "") # for logical operators need to use & | ~
print(f"Count of filtered rows: {df_filtered.count()}")

def get_metadata(data):
    return { "text_size": len(data["text"]), "metadata": { "active": True } }

struct_schema = StructType([
    StructField("text_size", IntegerType(), True),
    StructField("metadata", StructType([
        StructField("active", BooleanType(), True)
    ]), True)
])

get_metadata_udf = udf(get_metadata, struct_schema)

df_with_metadata = df_filtered.withColumn("metadata", get_metadata_udf(df_filtered["data"]))
df_with_metadata.limit(5).show(truncate=False)

df_with_metadata.select(
    col("id"),
    col("source"),
    col("data.category"),
    col("metadata.text_size"),
    col("metadata.metadata.active")
) \
.limit(10) \
.show(truncate=False)

# TODO: save the projected data into postgres
jdbc_url = "jdbc:postgresql://postgres-db:5432/postgres"
properties = {
    "user": "postgres",
    "password": "password",
    "driver": "org.postgresql.Driver"
}

df_with_metadata.select(
    col("id"),
    col("source"),
    col("data.category"),
    col("metadata.text_size"),
    col("metadata.metadata.active")
) \
.write.jdbc(url=jdbc_url, table="filtered_data", mode="overwrite", properties=properties)

spark.stop()