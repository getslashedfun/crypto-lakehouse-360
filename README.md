# Crypto Lakehouse 360

Lakehouse de dados de mercado cripto, de ponta a ponta: coleta de velas públicas da Binance, landing no Amazon S3, processamento em camadas Bronze, Silver e Gold no Databricks e entrega de indicadores, dashboard e um assistente que responde perguntas sobre os dados.

Projeto de estudo e portfólio, feito para praticar a migração de ETL tradicional (Oracle/ODI) para cloud com Databricks e PySpark e para cobrir o conteúdo da certificação **Databricks Certified Data Engineer Associate**.

## Stack

| Camada | Tecnologia |
|---|---|
| Fonte | Binance (API pública e arquivos históricos) |
| Coleta | Python, requests, Boto3, GitHub Actions |
| Landing | Amazon S3 |
| Lakehouse | Databricks Free Edition, Delta Lake, Unity Catalog |
| Pipelines | Lakeflow Spark Declarative Pipelines, Auto Loader, AUTO CDC |
| Orquestração | Lakeflow Jobs |
| Deploy | Declarative Automation Bundles, Databricks CLI, GitHub Actions |
| Consumo | Databricks SQL, dashboards AI/BI, Genie |

## Arquitetura

```
Binance → coletor Python → S3 (landing) → Volume UC → Bronze → Silver → Gold → dashboard / assistente
```

## Status

Sprint 0 (fundação) em andamento.

| Sprint | Tema | Status |
|---|---|---|
| 0 | Fundação: repositório, catálogo, conectividade, AWS | em andamento |
| 1 | Coletor REST e landing no S3 | |
| 2 | Bronze com Auto Loader | |
| 3 | Silver com expectations e AUTO CDC | |
| 4 | Gold: indicadores e score | |
| 5 | Lakeflow Jobs | |
| 6 | Governança e segurança | |
| 7 | Otimização e troubleshooting | |
| 8 | CI/CD | |
| 9 | Dashboard e assistente | |

## Documentação

- [Plano do projeto v2 (PDF)](docs/Documentacao_Crypto_Lakehouse_360_v2.pdf)
- [Roteiro do Sprint 0](docs/sprint-0.md)

## Limites

Uso educacional. Não executa ordens, não custodia ativos e não faz recomendação de investimento. Usa apenas dados públicos de mercado; nenhum dado pessoal real e nenhuma credencial ficam neste repositório.
