import boto3
import requests
import json
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

def fetch_serie(codigo: int, data_inicial: str, data_final: str) -> list:
    #faz a requisição e retorna os dados como lista
    url= f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    try:    
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        logger.info(f"Série {codigo} coletada com sucesso | {len(dados)} registros")
        return dados
    except Exception as e:
        logger.exception(f"Erro inesperado ao buscar série {codigo}: {e}")
        return []
    


def save_local(data: list, nome: str) -> str:
    # salva o JSON bruto em raw/ano/mes/dia/nome.json
    # retorna o caminho do arquivo salvo
    hoje = datetime.now()
    ano = hoje.strftime("%Y")
    mes = hoje.strftime("%m")
    dia = hoje.strftime("%d")

    path = os.path.join("raw", ano, mes, dia)

    os.makedirs(path, exist_ok=True)

    filepath = os.path.join(path, f"{nome}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False, indent=4)

    logger.info(f"Arquivo salvo em {filepath}")

    return filepath
    


def upload_to_s3(filepath: str, bucket: str, s3_key: str) -> None:
    # Faz upload do arquivo para o S3
    s3 = boto3.client(
        service_name = 's3',
        region_name = 'us-east-2'
    )
    s3.upload_file(filepath, bucket, s3_key)
    logger.info(f"Arquivo salvo em s3://{bucket}/{s3_key}")

dados = fetch_serie(432, '01/01/2024', '28/04/2026')
caminho = save_local(dados, 'selic')
s3_key = os.path.relpath(caminho).replace("\\", "/")
upload_to_s3(caminho, 'pipelinebcb', s3_key)