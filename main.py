import logging
import os
from src.extract import fetch_serie, save_local, upload_to_s3
from src.load import load
from src.transform import transform

logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s " 
                        )
logger = logging.getLogger(__name__)

BUCKET = "pipelinebcb"
data_inicial = '01/01/2024'
data_final = '28/04/2026'

SERIES = [
    {"codigo": 433, "nome": "ipca"},
    {"codigo": 432, "nome": "selic"}
]

def run():
    logger.info("Pipeline iniciado")
    for serie in SERIES:
        logger.info(f"Processando serie {serie["nome"]}")
        dados_brutos = fetch_serie(serie["codigo"], data_inicial, data_final)
        dados_transformados = transform(dados_brutos, serie["nome"])
        caminho = save_local(dados_brutos,serie["nome"])
        s3_key = os.path.relpath(caminho).replace("\\", "/")
        upload_to_s3(caminho, 'pipelinebcb', s3_key)
        #load(dados_transformados)
    logger.info("Pipeline finalizado")
if __name__ == "__main__":
    run()