# Databricks notebook source
import time
from datetime import datetime, timezone

import requests
from pyspark.sql.types import (IntegerType, StringType, StructField,
                               StructType, TimestampType)

dbutils.widgets.text("catalogo", "crypto360")
catalogo = dbutils.widgets.get("catalogo")

DOMINIOS = {
    "binance_api":  "https://data-api.binance.vision/api/v3/ping",
    "binance_hist": "https://data.binance.vision/",
    "kraken":       "https://api.kraken.com/0/public/Time",
    "coingecko":    "https://api.coingecko.com/api/v3/ping",
    "aws_s3":       "https://s3.amazonaws.com/",
    "github_api":   "https://api.github.com/",
}

# COMMAND ----------

linhas = []
for nome, url in DOMINIOS.items():
    inicio = time.time()
    try:
        resposta = requests.get(url, timeout=10)
        status, erro = resposta.status_code, None
    except Exception as e:
        status, erro = None, f"{type(e).__name__}: {str(e)[:200]}"
    latencia = int((time.time() - inicio) * 1000)
    linhas.append((datetime.now(timezone.utc), nome, url, status, latencia, erro))

schema = StructType([
    StructField("checked_at", TimestampType()),
    StructField("dominio", StringType()),
    StructField("url", StringType()),
    StructField("status_http", IntegerType()),
    StructField("latencia_ms", IntegerType()),
    StructField("erro", StringType()),
])

df = spark.createDataFrame(linhas, schema)
df.write.mode("append").saveAsTable(f"{catalogo}.ops.connectivity_check")
display(df)