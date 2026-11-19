# Sprint 0 · Fundação

Objetivo: ambiente pronto, versionado desde o primeiro commit, e saber de verdade o que o Free Edition alcança.
Domínios da prova: Plataforma (6%), CI/CD (10%), Governança (15%).

Legenda: **[você]** só você faz (conta, senha, clique) · **[juntos]** você escreve, eu explico e reviso.

Workspace: `https://dbc-9cb395bf-ae37.cloud.databricks.com` (conta Free Edition própria do projeto, separada do BTC-LAKEHOUSE).

## Passos

| # | Passo | Quem | Pronto quando |
|---|---|---|---|
| 1 | Repositório público `crypto-lakehouse-360` no GitHub, vazio | [você] | URL do repo existe |
| 2 | `git init` local em `Desktop\CRYPTO-LAKEHOUSE-360`, `.gitignore`, README, 1º commit e push | [juntos] | docs aparecem no GitHub |
| 3 | Git folder no workspace apontando para o repo | [você] | pasta aparece em Workspace > Home |
| 4 | Perfil `crypto360` no Databricks CLI (OAuth) | [você] | `databricks current-user me -p crypto360` responde |
| 5 | SQL: catálogo `crypto360`, schemas, volume `landing.raw` | [juntos] | `SHOW SCHEMAS IN crypto360` lista os 5 |
| 6 | `databricks.yml` mínimo + `bundle validate` + `deploy` | [juntos] | job aparece com prefixo `[dev ...]` |
| 7 | Notebook/job `conectividade` gravando em `ops.connectivity_check` | [juntos] | tabela com 1 linha por domínio |
| 8 | Conta AWS no Free Plan: MFA no root, usuário admin, Budgets US$ 1 | [você] | alerta criado |
| 9 | Bucket privado na região do workspace (Block Public Access, versionamento, SSE-S3, lifecycle 30 dias) | [juntos] | bucket criado |
| 10 | IAM: role OIDC para o GitHub Actions (PutObject em `landing/`) e policy de leitura para o Databricks | [juntos] | policies no repo em `infra/aws/` |
| 11 | Teste da ponte A (storage credential + external location) e, se falhar, B | [juntos] | ADR-004 escrito |
| 12 | `docs/decisions.md` com ADR 001 a 004 | [juntos] | arquivo no repo |

## Aceite do sprint

- Bundle implantado pelo CLI; catálogo, schemas e volume existem.
- `ops.connectivity_check` preenchida.
- Ponte S3 → Databricks escolhida e documentada.
- Nenhum segredo no Git (`.env`, `.databrickscfg`, chaves AWS fora do repositório).

## Perguntas para responder sem consultar no fim

1. Onde roda o serverless: na conta da Databricks ou na sua conta de nuvem? E o compute clássico?
2. Qual a diferença entre volume gerenciado e volume externo?
3. O que `bundle validate`, `bundle deploy` e `bundle run` fazem? Qual deles executa o job?
4. Qual o equivalente do contexto do ODI no bundle?
5. Por que OIDC é melhor que access key fixa no GitHub Actions?
