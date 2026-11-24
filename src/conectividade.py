# Databricks notebook source
# ^ Esta 1ª linha faz o Databricks abrir o .py como NOTEBOOK (e não como arquivo comum).
#   Vantagem sobre .ipynb: é texto puro, então o diff no Git fica legível.
#
# OBJETIVO: descobrir quais domínios da internet o compute serverless consegue alcançar
#           (o Free Edition restringe a saída) e guardar o resultado numa tabela Delta.
# SPRINT 0 · Prova: Plataforma (serverless), Unity Catalog (nome em 3 níveis), Jobs (parâmetros)

# --- Imports -------------------------------------------------------------------------
import time                                   # time.time() = segundos desde 1970; usamos para medir latência
from datetime import datetime, timezone       # datetime.now(timezone.utc) = agora em UTC (sempre UTC em dados!)

import requests                               # biblioteca para chamadas HTTP (GET, POST...)
from pyspark.sql.types import (               # tipos do Spark para declarar o schema da tabela
    IntegerType, StringType, StructField, StructType, TimestampType,
)

# --- Parâmetro -----------------------------------------------------------------------
# dbutils.widgets cria um campo de parâmetro no notebook (painel "Parameters").
#   - rodando à mão: vale o default "crypto360"
#   - rodando pelo job: o valor vem de base_parameters (resources/conectividade.job.yml),
#     que por sua vez vem de ${var.catalogo} no databricks.yml
# Prova: widget = como notebook recebe parâmetro; job parameter vence task parameter.
dbutils.widgets.text("catalogo", "crypto360")
catalogo = dbutils.widgets.get("catalogo")

# Dicionário Python: nome -> URL. Fica separado da lógica para facilitar incluir domínios.
DOMINIOS = {
    "binance_api":  "https://data-api.binance.vision/api/v3/ping",   # velas recentes (Sprint 1)
    "binance_hist": "https://data.binance.vision/",                  # histórico em ZIP (Sprint 1)
    "kraken":       "https://api.kraken.com/0/public/Time",          # 2ª fonte (Sprint 4)
    "coingecko":    "https://api.coingecko.com/api/v3/ping",         # market cap (opcional)
    "aws_s3":       "https://s3.amazonaws.com/",                     # ponte S3 -> Databricks (passo 11)
    "github_api":   "https://api.github.com/",                       # automação/CI
}

# COMMAND ----------
# ^ Separador de célula. No Databricks, cada bloco entre esses marcadores vira uma célula.

# --- Teste de cada domínio (Python puro: roda só no DRIVER, uma máquina) -------------
linhas = []                                   # lista Python que vai guardar uma tupla por domínio
for nome, url in DOMINIOS.items():            # .items() devolve pares (chave, valor) do dicionário
    inicio = time.time()
    try:
        # timeout=10: sem ele, uma URL travada prenderia o job até o limite de tempo do job
        resposta = requests.get(url, timeout=10)
        status, erro = resposta.status_code, None        # 200 = OK, 403 = proibido, 451 = bloqueio legal...
    except Exception as e:
        # Domínio bloqueado não derruba o job: o erro vira DADO na tabela.
        # (mesma ideia das expectations com "warn" no pipeline: registra e segue)
        status, erro = None, f"{type(e).__name__}: {str(e)[:200]}"   # f-string; [:200] corta o texto
    latencia = int((time.time() - inicio) * 1000)                    # segundos -> milissegundos
    linhas.append((datetime.now(timezone.utc), nome, url, status, latencia, erro))

# --- Schema explícito ----------------------------------------------------------------
# Por que declarar? Se TODOS os domínios responderem, a coluna "erro" fica toda None e o
# Spark não consegue adivinhar o tipo (erro de inferência). Declarando, o tipo é garantido.
# Prova: schema explícito x inferido; schema enforcement (Delta rejeita o que não bate).
schema = StructType([
    StructField("checked_at",  TimestampType()),   # quando testamos (UTC)
    StructField("dominio",     StringType()),
    StructField("url",         StringType()),
    StructField("status_http", IntegerType()),     # None quando nem chegou a responder
    StructField("latencia_ms", IntegerType()),
    StructField("erro",        StringType()),
])

# --- Daqui para baixo é SPARK (motor distribuído) ------------------------------------
# createDataFrame: converte a lista Python (no driver) num DataFrame do Spark.
df = spark.createDataFrame(linhas, schema)

# write.mode("append"): ACRESCENTA linhas, mantendo os testes anteriores (histórico).
#   "overwrite" substituiria tudo. Mais tarde usaremos MERGE / AUTO CDC para atualizar por chave.
# saveAsTable: cria a tabela se não existir. Sem LOCATION => tabela GERENCIADA, formato Delta.
#   Nome em 3 níveis: catalogo.schema.tabela  (Unity Catalog)
# Prova: DROP em tabela gerenciada apaga os dados; cada escrita vira uma versão (DESCRIBE HISTORY).
df.write.mode("append").saveAsTable(f"{catalogo}.ops.connectivity_check")

# display é uma AÇÃO: mostra o resultado. Avaliação preguiçosa = transformações só montam
# um plano; o Spark executa de fato quando aparece uma ação (display, count, write...).
display(df)
