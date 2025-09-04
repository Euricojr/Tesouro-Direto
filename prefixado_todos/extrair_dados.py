import tesouro_direto_br as td
from datetime import datetime
def extrair_dados_prefixado_qualquer_ano(index_titulo, dados_titulo):
    """
    Versão que funciona para qualquer ano (cópia da sua função original)
    """
    dados_extraidos = {
        'nome': index_titulo[0],
        'vencimento': index_titulo[1],
        'pu_biblioteca': float(dados_titulo['PU']),
        'valor_nominal': 1000.0,  # Padrão para Tesouro Prefixado
        'data_consulta': datetime.now().date()
    }
    
    # Converte vencimento para date se necessário
    if hasattr(dados_extraidos['vencimento'], 'date'):
        dados_extraidos['vencimento'] = dados_extraidos['vencimento'].date()
    elif isinstance(dados_extraidos['vencimento'], str):
        dados_extraidos['vencimento'] = datetime.strptime(dados_extraidos['vencimento'], "%Y-%m-%d").date()
    
    return dados_extraidos