def calcular_cotacao_selic(taxa_contratada, dias_uteis):
    """
    Calcula cotação do Tesouro Selic
    Cotação (%) = 100 / (1 + taxa_contratada)^(dias_uteis/252)
    
    Args:
        taxa_contratada (float): Taxa de ágio/deságio em decimal
        dias_uteis (int): Dias úteis até vencimento
    """
    expoente = dias_uteis / 252
    cotacao = 100 / ((1 + taxa_contratada) ** expoente)
    
    return cotacao