import logging
import os
from src.extract import fetch_serie, save_local, upload_to_s3, save_processed
from src.load import load
from src.transform import transform
import datetime

logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s " 
                        )
logger = logging.getLogger(__name__)

BUCKET = "pipelinebcb"
data_inicial = '01/01/2024'
data_final = datetime.now().strftime('%d/%m/%Y')

SERIES = [
    {"codigo": 433, "nome": "ipca"},
    {"codigo": 432, "nome": "selic"}
]

def run():
    logger.info("Pipeline iniciado")
    for serie in SERIES:
        logger.info(f"Processando serie {serie['nome']}")
        dados_brutos = fetch_serie(serie["codigo"], data_inicial, data_final)
        dados_transformados = transform(dados_brutos, serie["nome"])
        caminho_raw = save_local(dados_brutos,serie["nome"])
        s3_key_raw = os.path.relpath(caminho_raw).replace("\\", "/")
        upload_to_s3(caminho_raw, BUCKET, s3_key_raw)
        caminho_processed = save_processed(dados_transformados, serie["nome"])
        s3_key_processed = os.path.relpath(caminho_processed).replace("\\", "/")
        upload_to_s3(caminho_processed, BUCKET , s3_key_processed)
        load(dados_transformados)
    logger.info("Pipeline finalizado")
if __name__ == "__main__":
    run()