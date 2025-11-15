import os
import pathlib
import time

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

if __name__ == "__main__":
    os.makedirs("./delta", exist_ok=True)

    builder = (
        SparkSession.builder.appName("DeltaInit")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    data_path = pathlib.Path(__file__).parent.resolve().joinpath("data")
    delta_path = pathlib.Path(__file__).parent.resolve().joinpath("delta")
    tables = ["customers", "accounts", "branches", "transactions", "loans", "employees"]
    start = time.time()
    for table in tables:
        source = data_path.joinpath(f"{table}.parquet").as_posix()
        dest = delta_path.joinpath(table).as_posix()
        df = spark.read.parquet(source)
        df.write.format("delta").mode("overwrite").save(dest)
        spark.read.format("delta").load(dest).createOrReplaceTempView(table)
        print(f"Table {table} was processed (from {source} to {dest}), record count: {df.count()}")

    print("All tables were processed successfully.")
    print("Total time: ", round(time.time() - start, 2), " seconds")
    spark.stop()
