from datetime import datetime
import logging

logger = logging.getLogger(__name__)
def transform(data: list, nome: str) -> list:
    resultado = []

    for item in data:
        if not item.get("valor"):
            continue
        data_convertida = datetime.strptime(item["data"], "%d/%m/%Y")

        novo = {
            "data_referencia": data_convertida,
            "valor": float(item["valor"]),
            "serie": nome
        }
        
        resultado.append(novo)
    logger.info(f"Transformação Concluída | série: {nome} | {len(resultado)} registros")
    return resultado