# Pipeline ETL — Indicadores BCB (IPCA e Selic)

## Descrição
A pipeline foi desenvolvida para buscar dados (IPCA e Selic) via API do banco central do Brasil, carregados em um bucket no S3, transformados via python e feito load dos dados tratados em um banco de dados do postgres containerizado via Docker

## Arquitetura
```text
          API BCB (SGS)
               │
               ▼
         extract.py
               │
               ▼
 AWS S3 (raw/ano/mes/dia/serie.json)
               │
               ▼
        transform.py
               │
               ▼
AWS S3 (processed/ano/mes/dia/serie.json)
(Limpeza, tipagem e tratamento de anomalias)
               │
               ▼
           load.py
               │
               ▼
 PostgreSQL (Tabela: indicadores_bcb)
 (Full-load com carga idempotente (UPSERT))
```

# Tech Stack

| Camada | Tecnologia |
|---------|------------|
| Linguagem | Python 3.11 |
| Armazenamento | AWS S3 (RAW e PROCESSED) |
| Banco de Dados | PostgreSQL 15 |
| Infraestrutura | Docker + Docker Compose |
| CI / Testes | GitHub Actions + Pytest |
| Bibliotecas | boto3, psycopg2, requests |

---

# Destaques de Engenharia e Métricas

### Idempotência (UPSERT)

A tabela `indicadores_bcb` utiliza uma constraint `UNIQUE (data_referencia, serie)`. O pipeline utiliza `ON CONFLICT DO UPDATE`, garantindo **0 duplicatas** em reexecuções e atualizando automaticamente valores retroativos disponibilizados pelo Banco Central.

---

### Tratamento de Dados Reais

A API do Banco Central frequentemente retorna strings vazias (`""`) em dias não úteis. A camada de transformação remove esses registros antes da carga no banco de dados, evitando inconsistências.

---

### Datas Dinâmicas

A extração percorre automaticamente os dados históricos até o **D-0 (`datetime.now()`)**, eliminando a necessidade de hardcoding de datas e garantindo capturas diárias atualizadas.

---

### CI/CD Focada em Regras de Negócio

A esteira de **GitHub Actions** valida automaticamente a lógica de transformação a cada commit.

Os testes em **Pytest** utilizam **mocks** para simular falhas da API do Banco Central, assegurando que o tratamento de anomalias continue funcionando corretamente.

---

### Volume Processado

- **~876 registros processados por execução**
  - **849 registros da Selic**
  - **27 registros do IPCA**

---

# Como Rodar Localmente

## Pré-requisitos

- Docker Desktop instalado
- Conta AWS com bucket S3 configurado
- Arquivo `.env` configurado na raiz do projeto

---

## Variáveis de Ambiente (`.env`)

```env
DB_HOST=db-postgres
DB_PORT=5432
DB_NAME=pipeline_db
DB_USER=postgres
DB_PASSWORD=sua_senha

AWS_ACCESS_KEY_ID=sua_chave
AWS_SECRET_ACCESS_KEY=sua_chave_secreta
AWS_DEFAULT_REGION=us-east-2
```

---

## Execução

```bash
git clone https://github.com/GabrielDataLab/Pipeline-ETL-com-Python-AWS-S3-PostgreSQL-containerizado.git

cd Pipeline-ETL-com-Python-AWS-S3-PostgreSQL-containerizado

docker-compose up --build
```

---

# Estrutura do Repositório

```text
pipeline-bcb-etl/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de CI/CD (GitHub Actions)
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   └── test_pipeline.py        # Testes unitários (Pytest) com mocks da API
├── main.py
└── README.md
```
