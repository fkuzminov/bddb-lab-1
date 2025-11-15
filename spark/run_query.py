# spark_query.py
import argparse
import pathlib

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

queries_path = pathlib.Path(__file__).parent.resolve().joinpath("queries")
delta_path = pathlib.Path(__file__).parent.resolve().joinpath("delta")
TABLES = ["customers", "accounts", "branches", "transactions", "loans", "employees"]


def main(sql_file: str) -> None:
    sql_file_path = queries_path.joinpath(sql_file)
    with open(f"{sql_file_path}.sql", "r") as f:
        query = f.read().strip()

    builder = (
        SparkSession.builder.appName("DeltaQuery")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    for table in TABLES:
        if not table in query:
            continue
        print(f">> Loading table: {table}")
        spark.read.format("delta").load(delta_path.joinpath(table).as_posix()).createOrReplaceTempView(table)
    print(f">> Executing query from: {sql_file}")
    print(query)
    result = spark.sql(query)

    result.show(truncate=False)

    spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to SQL file (e.g. 01)")
    args = parser.parse_args()
    main(args.file)
