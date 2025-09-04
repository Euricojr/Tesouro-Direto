from datetime import datetime, timedelta

def obter_ultimo_dia_15(data_referencia):
    """
    Encontra o último dia 15 oficial antes da data de referência
    
    Args:
        data_referencia (datetime): Data de referência para buscar o último dia 15
        
    Returns:
        datetime: Data do último dia 15 oficial
    """
    ano = data_referencia.year
    mes = data_referencia.month
    
    # Se ainda não passou do dia 15 do mês atual, volta para o mês anterior
    if data_referencia.day < 15:
        if mes == 1:  # Se for janeiro, volta para dezembro do ano anterior
            mes = 12
            ano -= 1
        else:
            mes -= 1
    
    # Retorna o dia 15 do mês correto
    return datetime(ano, mes, 15)