import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col,year,month
from pyspark.sql.types import BooleanType

table = "bigquery-public-data:stackoverflow.stackoverflow_posts"

spark = SparkSession.builder \
    .appName("pyspark-example") \
    .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar") \
    .getOrCreate()

df = spark.read.format("bigquery").load(table)

df = df.filter(col("tags").isNotNull()) \
        .select(
            df.tags,
            year(df.creation_date).alias('post_year'), \
            month(df.creation_date).alias('post_month')
            ) \
        .groupBy(["tags","post_year","post_month"]) \
        .count() \
        .orderBy("count", ascending=False) \
        .limit(50) \
        .cache()

df.write.option("header", True).csv("gs://serverless-spark-udemy/test_output")