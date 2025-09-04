from datetime import datetime, timedelta
import requests
import pandas as pd
from função_obter_ultimo_dia_15 import obter_ultimo_dia_15

def calcular_vna_projetado(data_compra, ipca_projetado_mensal):
    """
    Calcula VNA projetado usando a fórmula do documento
    VNA projetado = VNA_último × (1+IPCA_projetado)^pr1
    """
    # Obter VNA do último dia 15
    data_ultimo_15 = obter_ultimo_dia_15(data_compra)
    
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
        r = requests.get(url)
        dados = pd.DataFrame(r.json())
        
        dados["data"] = pd.to_datetime(dados["data"], dayfirst=True)
        dados["valor"] = dados["valor"].astype(float) / 100
        
        inicio = pd.to_datetime("2000-07-01")
        ipca_ate_ultimo_15 = dados[(dados["data"] >= inicio) & (dados["data"] <= data_ultimo_15)]
        
        fator = (1 + ipca_ate_ultimo_15["valor"]).prod()
        vna_ultimo_15 = 1000 * fator
        
    except Exception as e:
        print(f"❌ Erro ao calcular VNA do último dia 15: {e}")
        return None
    
    # Calcular pr1 (proporção dos dias)
    if data_compra.day >= 15:
        dia_15_atual = datetime(data_compra.year, data_compra.month, 15)
        if data_compra.month == 12:
            proximo_15 = datetime(data_compra.year + 1, 1, 15)
        else:
            proximo_15 = datetime(data_compra.year, data_compra.month + 1, 15)
    else:
        dia_15_atual = data_ultimo_15
        proximo_15 = datetime(data_compra.year, data_compra.month, 15)
    
    dias_desde_ultimo_15 = (data_compra - dia_15_atual).days
    dias_total_periodo = (proximo_15 - dia_15_atual).days
    pr1 = dias_desde_ultimo_15 / dias_total_periodo if dias_total_periodo > 0 else 0
    
    # Calcular VNA projetado
    vna_projetado = vna_ultimo_15 * (1 + ipca_projetado_mensal) ** pr1
    
    return vna_projetado



