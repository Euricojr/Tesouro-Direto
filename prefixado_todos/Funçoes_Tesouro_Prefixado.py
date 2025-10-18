
import tesouro_direto_br as td
from datetime import datetime



def buscar_titulos_prefixados():
    """
    Busca TODOS os títulos Tesouro Prefixado disponíveis
    Retorna uma lista com todos os prefixados encontrados
    """
    try:
        # Busca todos os títulos:
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
                #print(f"🎯 TÍTULO ENCONTRADO!")
                #print(f"Nome: {index[0]}")
                #print(f"Vencimento: {index[1]}")
                #print(f"PU: R$ {dados['PU']:,.6f}")
                
                return index, dados
            elif str(ano_vencimento) in str(vencimento):
                ##print(f"🎯 TÍTULO ENCONTRADO!")
                #rint(f"Nome: {index[0]}")
                #print(f"Vencimento: {index[1]}")
                #print(f"PU: R$ {dados['PU']:,.6f}")
                
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

def calcular_dias_uteis(data_atual, data_vencimento):
    """
    Calcula dias úteis entre duas datas (aproximação usando 252 dias úteis/ano)
    """
    dias_corridos = (data_vencimento - data_atual).days
    dias_uteis = int(dias_corridos * (252 / 365))
    return dias_uteis, dias_corridos

def calcular_pu_prefixado_oficial(vn, taxa_anual, du):
    """
    Fórmula oficial do Tesouro Direto para títulos prefixados:
    PU = VN / [(Taxa/100 + 1)^(du/252)]
    """
    base = (taxa_anual / 100) + 1
    expoente = du / 252
    pu = vn / (base ** expoente)
    return pu




def calculadora_prefixado_por_ano(ano, taxa_anual):
    """
    Calculadora para qualquer ano de prefixado
    Baseada na sua calculadora original
    
    Args:
        ano (int): Ano do vencimento (ex: 2032)
        taxa_anual (float): Taxa anual do título (ex: 13.92)
    """
    print(f"🚀 CALCULADORA TESOURO PREFIXADO {ano}")
    print("=" * 60)
    
    # Passo 1: Buscar o título usando seu buscador
    index_titulo, dados_titulo = buscar_prefixado_por_ano(ano)
    
    if index_titulo is None:
        print(f"❌ Não foi possível encontrar o Prefixado {ano}. Verifique se está disponível.")
        return None
    
    # Passo 2: Extrair dados
    dados = extrair_dados_prefixado_qualquer_ano(index_titulo, dados_titulo)
    
    #print(f"\n📋 DADOS EXTRAÍDOS:")
    #print(f"Título: {dados['nome']}")
    print(f"Vencimento: {dados['vencimento']}")
    #print(f"PU da Biblioteca: R$ {dados['pu_biblioteca']:,.6f}")
    #print(f"Valor Nominal: R$ {dados['valor_nominal']:,.2f}")
    
    # Passo 3: Calcular dias úteis
    du, dias_corridos = calcular_dias_uteis(dados['data_consulta'], dados['vencimento'])
    
    #print(f"\n📅 CÁLCULO DE PRAZO:")
    #print(f"Data atual: {dados['data_consulta']}")
    #print(f"Data vencimento: {dados['vencimento']}")
    #print(f"Dias corridos: {dias_corridos}")
    #print(f"Dias úteis (du): {du}")
    
    # Passo 4: Usar a taxa informada
    print(f"\n🔢 USANDO TAXA: {taxa_anual}% a.a.")
    
    # Passo 5: Calcular PU usando a fórmula oficial
    pu_calculado = calcular_pu_prefixado_oficial(
        dados['valor_nominal'], 
        taxa_anual, 
        du
    )
 
    print(f"PU Calculado:     R$ {pu_calculado:,.6f}")
calculadora_prefixado_por_ano(ano=int(input("digite o ano:")), taxa_anual=float(input("digite a taxa:")))  
   



