
def calcular_dias_uteis(data_atual, data_vencimento):
    """
    Calcula dias úteis entre duas datas (aproximação usando 252 dias úteis/ano)
    """
    dias_corridos = (data_vencimento - data_atual).days
    dias_uteis = int(dias_corridos * (252 / 365))
    return dias_uteis, dias_corridos