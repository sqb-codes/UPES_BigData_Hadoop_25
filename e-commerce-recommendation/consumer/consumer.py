from pyspark.sql import SparkSession
from pyspark.sql.functions import  col, from_json, count, window
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

# Convert timestamp to proper time
from pyspark.sql.functions import to_timestamp
parsed_df = parsed_df.withColumn(
    "event_time",
    to_timestamp(col("timestamp"))
).withWatermark("event_time", "2 minutes")

filtered_df = parsed_df.filter(
    col("event_type").isin("view", "click", "add_to_cart", "search")
)

# Trending products
# Count events per product in last 1 minute window
trending_df = filtered_df \
    .groupby(
    window(col("event_time"), "1 minute"),
    col("product_id")
) \
    .agg(
    count("*").alias("event_count")
)

# User Based Recommendation
user_activity_df = filtered_df \
    .groupby("user_id", "product_id") \
    .agg(count("*").alias("interaction_count"))


def write_to_mongo(collection):
    def _write(df, _epoch_id):
        df.write \
            .format("mongodb") \
            .mode("append") \
            .option("spark.mongodb.connection.uri", "mongodb://mongodb:27017/") \
            .option("spark.mongodb.database", "e-comm-stream") \
            .option("spark.mongodb.collection", collection) \
            .save()
    return _write

trending_query = trending_df.writeStream \
    .foreachBatch(write_to_mongo("trending")) \
    .outputMode("update") \
    .option("checkpointLocation", "/tmp/spark-checkpoint/trending") \
    .start()

user_query = user_activity_df.writeStream \
    .foreachBatch(write_to_mongo("user_activity")) \
    .outputMode("update") \
    .option("checkpointLocation", "/tmp/spark-checkpoint/user_activity") \
    .start()

# # Print Trending Products
# trending_query = trending_df.writeStream \
#     .outputMode("complete") \
#     .format("console") \
#     .option("truncate",False) \
#     .start()
#
# # Print Trending Products
# user_query = user_activity_df.writeStream \
#     .outputMode("complete") \
#     .format("console") \
#     .option("truncate",False) \
#     .start()

# Keep streaming running
spark.streams.awaitAnyTermination()
