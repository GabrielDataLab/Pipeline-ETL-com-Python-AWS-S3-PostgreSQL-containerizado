import requests
requisicao = requests.get('https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json&dataInicial=01/01/2024&dataFinal=28/04/2026')
print(requisicao)
print(requisicao.json())           