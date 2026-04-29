# Pipeline ETL — Indicadores BCB (IPCA e Selic)

## Descrição
A pipeline foi desenvolvida para buscar dados (IPCA e Selic) via API do banco central do Brasil, carregados em um bucket no S3, transformados via python e feito load dos dados tratados em um banco de dados do postgres containnnerizado via Docker

## Arquitetura
API BCB (SGS)
│
▼
extract.py ──► S3 (raw/ano/mes/dia/)
│
▼
transform.py ──► S3 (processed/ano/mes/dia/)
│
▼
load.py ──► PostgreSQL (indicadores_bcb)

## Tecnologias
- Python 3.11
- AWS S3
- PostgreSQL 15
- Docker / Docker Compose
- boto3
- psycopg2
- python-dotenv

## Métricas
- **876 registros** processados por execução (849 Selic + 27 IPCA)
- **0 duplicatas** — pipeline idempotente com upsert por `data_referencia + serie`

## Como rodar localmente

### Pré-requisitos
- Docker Desktop instalado
- Conta AWS com bucket S3 configurado
- Arquivo `.env` na raiz com as variáveis abaixo

### Variáveis de ambiente (.env)
DB_HOST=db-postgres
DB_PORT=5432
DB_NAME=pipeline_db
DB_USER=postgres
DB_PASSWORD=sua_senha
AWS_ACCESS_KEY_ID=sua_chave
AWS_SECRET_ACCESS_KEY=sua_chave_secreta
AWS_DEFAULT_REGION=us-east-2

### Execução
```bash
git clone https://github.com/GabrielDataLab/Pipeline-ETL-com-Python-AWS-S3-PostgreSQL-containerizado
cd Pipeline-ETL-com-Python-AWS-S3-PostgreSQL-containerizado
docker-compose up --build
```

## Estrutura do repositório
pipeline-bcb-etl/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── main.py
└── README.md