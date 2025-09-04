import requests
import pandas as pd
from datetime import datetime

def calcular_vna():
    """
    Calcula o VNA (Valor Nominal Atualizado) automaticamente até hoje.
    Base: R$ 1.000,00 em 15/07/2000 corrigido pelo IPCA.
    """
    # Série 433 = IPCA (variação % mensal) no SGS do Bacen
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
    r = requests.get(url)
    dados = pd.DataFrame(r.json())
    
    # Preparar os dados
    dados["data"] = pd.to_datetime(dados["data"], dayfirst=True)
    dados["valor"] = dados["valor"].astype(float) / 100  # converte % para fração
    
    # Intervalo: de jul/2000 até hoje
    inicio = pd.to_datetime("2000-07-01")
    hoje = datetime.today()
    
    ipca = dados[(dados["data"] >= inicio) & (dados["data"] <= hoje)]
    
    # Calcula o fator acumulado
    fator = (1 + ipca["valor"]).prod()
    vna = 1000 * fator
    
    return vna

# -------------------------------
vna_hoje = calcular_vna()
#print(f"📊 VNA atualizado em {datetime.today().date()}: R$ {vna_hoje:,.2f}")
