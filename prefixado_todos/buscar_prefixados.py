import tesouro_direto_br as td
from datetime import datetime


def buscar_titulos_prefixados():
    """
    Busca TODOS os títulos Tesouro Prefixado disponíveis
    Retorna uma lista com todos os prefixados encontrados
    """
    try:
        # Busca todos os títulos
        todos_titulos = td.busca_tesouro_direto()
        
        # ✅ COMENTOU ESTE PRINT
        # print(f"✅ Total de títulos encontrados: {len(todos_titulos)}")
        
        # Filtra apenas os Prefixados
        titulos_prefixados = []
        
        for index, row in todos_titulos.iterrows():
            # O index pode ser uma tupla (nome, vencimento)
            if isinstance(index, tuple):
                nome_titulo = str(index[0]).lower()
                
                # Verifica se é Prefixado
                if 'prefixado' in nome_titulo:
                    titulos_prefixados.append((index, row))
        
        return titulos_prefixados
            
    except Exception as e:
        print(f"❌ Erro ao buscar títulos: {e}")
        return []


def buscar_prefixado_por_ano(ano_vencimento):
    """
    Busca um Tesouro Prefixado específico por ano de vencimento
    
    Args:
        ano_vencimento (int): Ano do vencimento desejado (ex: 2032)
    
    Returns:
        tuple: (index, dados) do título encontrado ou (None, None)
    """
    try:
        # Busca todos os prefixados
        titulos_prefixados = buscar_titulos_prefixados()
        
        if not titulos_prefixados:
            return None, None
        
        # Procura pelo ano específico
        for index, dados in titulos_prefixados:
            vencimento = index[1]
            
            # Verifica se o ano coincide
            if hasattr(vencimento, 'year') and vencimento.year == ano_vencimento:
                print(f"🎯 TÍTULO ENCONTRADO!")
                print(f"Nome: {index[0]}")
                print(f"Vencimento: {index[1]}")
                print(f"PU: R$ {dados['PU']:,.6f}")
                
                return index, dados
            elif str(ano_vencimento) in str(vencimento):
                print(f"🎯 TÍTULO ENCONTRADO!")
                print(f"Nome: {index[0]}")
                print(f"Vencimento: {index[1]}")
                print(f"PU: R$ {dados['PU']:,.6f}")
                
                return index, dados
        
        print(f"❌ Tesouro Prefixado {ano_vencimento} não encontrado")
        print(f"\nAnos disponíveis:")
        
        anos_disponiveis = set()
        for index, dados in titulos_prefixados:
            vencimento = index[1]
            if hasattr(vencimento, 'year'):
                anos_disponiveis.add(vencimento.year)
            elif isinstance(vencimento, str):
                try:
                    ano = int(vencimento[:4])
                    anos_disponiveis.add(ano)
                except:
                    pass
        
        for ano in sorted(anos_disponiveis):
            print(f"- {ano}")
        
        return None, None
        
    except Exception as e:
        print(f"❌ Erro ao buscar título: {e}")
        return None, None


def listar_prefixados_disponiveis():
    """
    Lista todos os prefixados disponíveis de forma organizada
    """
    print("📋 LISTAGEM DE TODOS OS PREFIXADOS DISPONÍVEIS")
    print("=" * 60)
    
    titulos_prefixados = buscar_titulos_prefixados()
    
    if not titulos_prefixados:
        print("Nenhum título encontrado.")
        return
    
    # Organiza por ano
    por_ano = {}
    for index, dados in titulos_prefixados:
        vencimento = index[1]
        ano = None
        
        if hasattr(vencimento, 'year'):
            ano = vencimento.year
        elif isinstance(vencimento, str):
            try:
                ano = int(vencimento[:4])
            except:
                ano = "Indefinido"
        
        if ano not in por_ano:
            por_ano[ano] = []
        por_ano[ano].append((index, dados))
    
    # Exibe organizadamente
    for ano in sorted(por_ano.keys()):
        print(f"\n📅 ANO {ano}:")
        for index, dados in por_ano[ano]:
            print(f"   • {index[0]} - Venc: {index[1]} - PU: R$ {dados['PU']:,.6f}")


# Funções de conveniência (para manter compatibilidade)
def buscar_tesouro_prefixado_2032():
    """
    Função específica para o 2032 (mantém compatibilidade com código antigo)
    """
    return buscar_prefixado_por_ano(2032)


def buscar_tesouro_prefixado_2031():
    """
    Função específica para o 2031
    """
    return buscar_prefixado_por_ano(2031)


def buscar_tesouro_prefixado_2029():
    """
    Função específica para o 2029
    """
    return buscar_prefixado_por_ano(2029)