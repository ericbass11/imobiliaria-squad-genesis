import requests

def get_real_time_rates():
    """
    Busca as taxas SELIC (432) e IPCA (433) do Banco Central.
    Retorna um dicionário com os valores e status.
    """
    endpoints = {
        'selic': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json',
        'ipca': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json'
    }

    rates = {'selic': 11.25, 'ipca': 4.5, 'status': 'estimated'}

    try:
        # Busca SELIC
        resp_selic = requests.get(endpoints['selic'], timeout=5)
        if resp_selic.status_code == 200:
            data = resp_selic.json()
            rates['selic'] = float(data[0]['valor'])

        # Busca IPCA
        resp_ipca = requests.get(endpoints['ipca'], timeout=5)
        if resp_ipca.status_code == 200:
            data = resp_ipca.json()
            rates['ipca'] = float(data[0]['valor'])
        
        rates['status'] = 'updated'

    except Exception as e:
        print(f"Erro ao buscar taxas do BCB: {e}")
    
    return rates
