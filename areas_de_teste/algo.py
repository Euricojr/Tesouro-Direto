import requests
import pandas as pd
from datetime import datetime, timedelta
import calendar

def obter_ultimo_vna_oficial(data_referencia):
    """
    Obtém o VNA oficial do último dia 15 anterior à data de referência.
    """
    # Para simplificar, vamos usar o VNA calculado até o último dia 15
    ano = data_referencia.year
    mes = data_referencia.month
    
    # Se estamos antes do dia 15 do mês atual, o último VNA oficial é do mês anterior
    if data_referencia.day < 15:
        if mes == 1:
            mes = 12
            ano -= 1
        else:
            mes -= 1
    
    # Data do último VNA oficial (dia 15)
    data_ultimo_vna = datetime(ano, mes, 15)
    
    # Calcula VNA até essa data
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
    r = requests.get(url)
    dados = pd.DataFrame(r.json())
    
    dados["data"] = pd.to_datetime(dados["data"], dayfirst=True)
    dados["valor"] = dados["valor"].astype(float) / 100
    
    inicio = pd.to_datetime("2000-07-01")
    ipca_ate_data = dados[(dados["data"] >= inicio) & (dados["data"] <= data_ultimo_vna)]
    
    fator = (1 + ipca_ate_data["valor"]).prod()
    vna_ultimo = 1000 * fator
    
    return vna_ultimo, data_ultimo_vna


def calcular_vna_projetado(data_compra, ipca_projetado_mensal):
    """
    Calcula o VNA projetado conforme fórmula do documento:
    VNA projetado = VNA × (1+IPCA projetado)^pr1
    
    onde pr1 = (dias entre compra e dia 15 atual) / (dias entre dia 15 atual e próximo dia 15)
    """
    # Obter o último VNA oficial
    vna_ultimo, data_ultimo_vna = obter_ultimo_vna_oficial(data_compra)
    
    # Calcular as datas do dia 15 atual e próximo
    if data_compra.day >= 15:
        # Próximo dia 15 é do mês seguinte
        if data_compra.month == 12:
            proximo_15 = datetime(data_compra.year + 1, 1, 15)
        else:
            proximo_15 = datetime(data_compra.year, data_compra.month + 1, 15)
        dia_15_atual = datetime(data_compra.year, data_compra.month, 15)
    else:
        # Ainda estamos no período do mês anterior
        dia_15_atual = data_ultimo_vna
        proximo_15 = datetime(data_compra.year, data_compra.month, 15)
    
    # Calcular pr1
    dias_desde_ultimo_15 = (data_compra - dia_15_atual).days
    dias_total_periodo = (proximo_15 - dia_15_atual).days
    pr1 = dias_desde_ultimo_15 / dias_total_periodo
    
    # Calcular VNA projetado
    vna_projetado = vna_ultimo * (1 + ipca_projetado_mensal) ** pr1
    
    return vna_projetado
