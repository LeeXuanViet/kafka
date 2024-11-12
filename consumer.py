from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

# Khởi tạo SparkSession
spark = SparkSession.builder \
    .appName("StockTransactionProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .config("spark.executor.extraJavaOptions", "-Dscala.usejavacp=true") \
    .getOrCreate()


# Định nghĩa schema cho dữ liệu giao dịch chứng khoán
schema = StructType([
    StructField("transaction_id", IntegerType(), True),
    StructField("stock_symbol", StringType(), True),
    StructField("price", FloatType(), True),
    StructField("volume", IntegerType(), True)
])

# Đọc dữ liệu từ Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "stock-transactions") \
    .load()

# Chuyển đổi dữ liệu Kafka từ định dạng nhị phân sang chuỗi JSON và áp dụng schema
transactions = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Hiển thị dữ liệu trên console
query = transactions.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
