from datetime import datetime
from src.transform import transform

def test_transformacao_limpeza_de_dados():
    # 1. Preparação (Arrange): Simulamos o JSON sujo que vem da API do BCB
    dados_mock_api = [
        {"data": "01/01/2024", "valor": "10.5"},
        {"data": "02/01/2024", "valor": ""}, # Valor vazio (comum no BCB nos finais de semana)
        {"data": "03/01/2024", "valor": "10.6"}
    ]
    
    # 2. Ação (Act): Passamos o mock pela SUA função de transformação
    resultado = transform(dados_mock_api, "selic")

    # 3. Validação (Assert): Verificamos se o seu código fez o trabalho
    
    # O valor vazio deve ter sido sumariamente ignorado (eram 3, devem sobrar 2)
    assert len(resultado) == 2 
    
    # A estrutura do dicionário deve ter sido alterada para o padrão do banco
    item_processado = resultado[0]
    
    assert "data_referencia" in item_processado
    assert item_processado["serie"] == "selic"  # Injetou o nome da série?
    assert isinstance(item_processado["valor"], float)  # Converteu a string para float?
    assert item_processado["valor"] == 10.5  # O valor está correto?
    
    # A string de data virou um objeto datetime válido?
    assert isinstance(item_processado["data_referencia"], datetime)
    assert item_processado["data_referencia"].year == 2024
    assert item_processado["data_referencia"].month == 1