from pyspark.sql import SparkSession
from pyspark.sql.functions import  col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType

spark = SparkSession.builder.appName("Kafka Spark Consumer").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read from Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "clickstream") \
    .option("startingOffsets", "latest") \
    .load()

# Kafka value is in binary -> Convert to string
df = df.selectExpr("CAST(value AS STRING)")

schema = StructType() \
    .add("user_id", IntegerType()) \
    .add("product_id", IntegerType()) \
    .add("event_type", StringType()) \
    .add("timestamp", DoubleType())


parsed_df = df.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

filtered_df = parsed_df.filter(
    col("event_type").isin("view", "click", "add_to_cart", "search")
)

query = filtered_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
