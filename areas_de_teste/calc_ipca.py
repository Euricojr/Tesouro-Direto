import requests
import pandas as pd
from datetime import datetime, timedelta
import calendar

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

def calcular_dias_uteis(data_inicio, data_fim):
    """
    Calcula o número de dias úteis entre duas datas.
    Para simplificar, considera apenas sábados e domingos como não úteis.
    """
    dias_uteis = 0
    data_atual = data_inicio
    
    while data_atual < data_fim:
        # Segunda=0, Domingo=6
        if data_atual.weekday() < 5:  # Segunda a sexta
            dias_uteis += 1
        data_atual += timedelta(days=1)
    
    return dias_uteis

def calcular_cotacao(taxa_contratada_aa, dias_uteis_vencimento):
    """
    Calcula a cotação conforme fórmula do documento:
    Cotação (%) = 100 / (1 + taxa_contratada)^(dias_úteis_vencimento / 252)
    """
    cotacao = 100 / ((1 + taxa_contratada_aa) ** (dias_uteis_vencimento / 252))
    return cotacao

def calcular_preco_ntnb(data_compra, data_vencimento, taxa_contratada_aa, ipca_projetado_mensal=0.005):
    """
    Calcula o preço de compra de uma NTN-B Principal.
    
    Parâmetros:
    - data_compra: datetime - Data da compra
    - data_vencimento: datetime - Data de vencimento do título
    - taxa_contratada_aa: float - Taxa real anual contratada (ex: 0.0613 para 6,13%)
    - ipca_projetado_mensal: float - IPCA projetado mensal (padrão 0.5%)
    
    Retorna:
    - dict com VNA projetado, cotação e preço final
    """
    
    # 1. Calcular VNA projetado
    vna_projetado = calcular_vna_projetado(data_compra, ipca_projetado_mensal)
    
    # 2. Calcular dias úteis até o vencimento
    dias_uteis = calcular_dias_uteis(data_compra, data_vencimento)
    
    # 3. Calcular cotação
    cotacao = calcular_cotacao(taxa_contratada_aa, dias_uteis)
    
    # 4. Calcular preço final
    preco = vna_projetado * (cotacao / 100)
    
    return {
        'vna_projetado': vna_projetado,
        'cotacao_percentual': cotacao,
        'dias_uteis_vencimento': dias_uteis,
        'preco_compra': preco
    }

#print(calcular_preco_ntnb(data_compra=input("Data compra (AAAA-MM-DD): "),data_vencimento=input("Data vencimento (AAAA-MM-DD): "),taxa_contratada_aa=float(input("Taxa contratada (ex: 0.0613 para 6,13%): "))), ipca_projetado_mensal= input("IPCA projetado mensal (ex: 0.005 para 0,5%): "))

2025


print(calcular_preco_ntnb(data_compra=datetime(2025,9,4),data_vencimento=datetime(2040,8,15),taxa_contratada_aa=0.0731, ipca_projetado_mensal=0.0059))  




# -------------------------------
# EXEMPLO DE USO
# -------------------------------
