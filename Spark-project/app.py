from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import col, count, sum
from pyspark.sql.types import StructType, StringType, IntegerType

# Create Spark Session
spark = SparkSession.builder.appName("E-comm pipeline").master("local[*]").getOrCreate()

# Initiate logging
spark.sparkContext.setLogLevel("ERROR")

orders_data = [
    Row(order_id=1, user_id=101, product_id=1001, amount=5000, category="Electronics"),
    Row(order_id=2, user_id=102, product_id=1090, amount=3000, category="Clothing"),
    Row(order_id=3, user_id=104, product_id=1086, amount=8000, category="Electronics"),
    Row(order_id=4, user_id=101, product_id=1011, amount=7000, category="Books")
]

orders_df = spark.createDataFrame(orders_data)

# streaming data (clickstream)
stream = StructType().add('user_id', IntegerType()) \
        .add('product_id', IntegerType()) \
        .add('event_type', StringType())

clickstream_df = spark.readStream.schema(stream).json('input_stream')

# Transformations
clean_df = clickstream_df.dropna()

filtered_df = clean_df.filter(
    col('event_type').isin('view', 'click')
)

joined_df = filtered_df.join(
    orders_df, on="product_id", how="inner"
)

# Aggregation
result_df = joined_df.groupBy('product_id').agg(
    count("event_type").alias("Total_events"),
    sum("amount").alias("total_revenue")
)

# Output to Console
query = result_df.writeStream.outputMode("complete").format("console").start()

query.awaitTermination()