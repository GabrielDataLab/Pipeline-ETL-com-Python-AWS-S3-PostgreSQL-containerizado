import os
from dotenv import load_dotenv
import psycopg2
import logging
logger = logging.getLogger(__name__)

load_dotenv()
def load(data: list) -> None:
    con = psycopg2.connect(
        host=os.getenv("DB_HOST"), 
        database=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"),
        )
    con.autocommit = True
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS indicadores_bcb(
                id SERIAL PRIMARY KEY,
                data_referencia DATE NOT NULL,
                valor FLOAT NOT NULL,
                serie VARCHAR(50) NOT NULL 
                )""")
    cur.executemany("INSERT INTO indicadores_bcb (data_referencia, valor, serie) VALUES (%s, %s, %s)", [(item["data_referencia"], item["valor"], item["serie"]) for item in data])
    con.commit()
    logging.info(f"{len(data)} registros inseridos na tabela indicadores_bcb")
    cur.close()
    con.close()