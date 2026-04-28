import requests
requisicao_selic = requests.get('https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json&dataInicial=01/01/2024&dataFinal=28/04/2026')
print(requisicao_selic)
print(requisicao_selic.json())

requisicao_ipca = requests.get('https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial=01/01/2024&dataFinal=28/04/2026')
print(requisicao_ipca)
print(requisicao_ipca.json())