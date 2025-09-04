from buscar_prefixados import buscar_prefixado_por_ano
from extrair_dados import extrair_dados_prefixado_qualquer_ano     
from calcular_dias_uteis import calcular_dias_uteis
from calcular_pu_prefixado import calcular_pu_prefixado_oficial



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
    
    print(f"\n📋 DADOS EXTRAÍDOS:")
    print(f"Título: {dados['nome']}")
    print(f"Vencimento: {dados['vencimento']}")
    print(f"PU da Biblioteca: R$ {dados['pu_biblioteca']:,.6f}")
    print(f"Valor Nominal: R$ {dados['valor_nominal']:,.2f}")
    
    # Passo 3: Calcular dias úteis
    du, dias_corridos = calcular_dias_uteis(dados['data_consulta'], dados['vencimento'])
    
    print(f"\n📅 CÁLCULO DE PRAZO:")
    print(f"Data atual: {dados['data_consulta']}")
    print(f"Data vencimento: {dados['vencimento']}")
    print(f"Dias corridos: {dias_corridos}")
    print(f"Dias úteis (du): {du}")
    
    # Passo 4: Usar a taxa informada
    print(f"\n🔢 USANDO TAXA: {taxa_anual}% a.a.")
    
    # Passo 5: Calcular PU usando a fórmula oficial
    pu_calculado = calcular_pu_prefixado_oficial(
        dados['valor_nominal'], 
        taxa_anual, 
        du
    )
    
    # Passo 6: Comparar resultados
    print(f"\n📊 COMPARAÇÃO DE RESULTADOS:")
    print("-" * 40)
    print(f"PU da Biblioteca: R$ {dados['pu_biblioteca']:,.6f}")
    print(f"PU Calculado:     R$ {pu_calculado:,.6f}")
    
    diferenca = abs(dados['pu_biblioteca'] - pu_calculado)
    diferenca_percent = (diferenca / dados['pu_biblioteca']) * 100
    
    print(f"Diferença:        R$ {diferenca:,.6f}")
    print(f"Diferença %:      {diferenca_percent:.4f}%")
    
    # Análise do resultado
    print(f"\n🎯 ANÁLISE:")
    if diferenca < 0.01:
        print("✅ EXCELENTE! Os valores estão praticamente idênticos!")
        print("A fórmula está correta!")
    elif diferenca < 1.5:
        print("✅ MUITO BOM! Diferença mínima, provavelmente devido a arredondamentos.")
    else:
        print("⚠️  DIFERENÇA SIGNIFICATIVA!")
        print("Possíveis causas:")
        print("- Taxa informada está incorreta")
        print("- Cálculo de dias úteis diferente")
        print("- Método de arredondamento diferente")
    
    return dados, pu_calculado


def calculadora_todos_prefixados_com_taxas():
    """
    Calcula todos os prefixados disponíveis
    Pede as taxas para o usuário ou usa taxas pré-definidas
    """
    print("🚀 CALCULADORA PARA TODOS OS PREFIXADOS")
    print("=" * 70)
    
    # Primeiro, descobre quais anos estão disponíveis
    from prefixado_todos.calculadora_prefixados import buscar_titulos_prefixados
    
    titulos_prefixados = buscar_titulos_prefixados()
    
    if not titulos_prefixados:
        print("❌ Nenhum prefixado encontrado.")
        return
    
    # Extrai os anos únicos
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
    
    anos_ordenados = sorted(anos_disponiveis)
    
    print(f"📅 ANOS DISPONÍVEIS: {', '.join(map(str, anos_ordenados))}")
    print("\n⚠️  IMPORTANTE: Você precisa informar as taxas!")
    print("Vá no site do Tesouro Direto e anote as taxas de cada prefixado.")
    
    # Coleta as taxas
    taxas = {13.90}
    
    for ano in anos_ordenados:
        while True:
            try:
                taxa_input = input(f"\n📊 Taxa do Prefixado {ano} (ex: 13.92): ")
                taxa = float(taxa_input.replace(',', '.'))
                taxas[ano] = taxa
                break
            except ValueError:
                print("❌ Digite um número válido (ex: 13.92 ou 13,92)")
            except KeyboardInterrupt:
                print("\n👋 Operação cancelada.")
                return
    
    # Agora calcula todos
    resultados = []
    
    for ano in anos_ordenados:
        print(f"\n{'='*70}")
        resultado = calculadora_prefixado_por_ano(ano, taxas[ano])
        if resultado:
            resultados.append({
                'ano': ano,
                'taxa': taxas[ano],
                'dados': resultado[0],
                'pu_calculado': resultado[1]
            })
    
    # Resumo final
    print(f"\n{'='*70}")
    print("📊 RESUMO GERAL")
    print("="*70)
    
    for resultado in resultados:
        dados = resultado['dados']
        diferenca = abs(dados['pu_biblioteca'] - resultado['pu_calculado'])
        diferenca_percent = (diferenca / dados['pu_biblioteca']) * 100
        
        status = "✅" if diferenca < 1.5 else "⚠️"
        
        print(f"{status} Prefixado {resultado['ano']}: ")
        print(f"    Taxa: {resultado['taxa']:.2f}% | Diferença: {diferenca_percent:.4f}%")
    
    return resultados


def calculadora_prefixado_interativa():
    """
    Versão interativa - escolhe um ano e pede a taxa
    """
    print("🎯 CALCULADORA INTERATIVA - PREFIXADO")
    print("=" * 50)
    
    # Pede o ano
    ano = int(input("📅 Digite o ano do Prefixado (ex: 2032): "))
    
    # Pede a taxa
    while True:
        try:
            taxa_input = input(f"📊 Digite a taxa do Prefixado {ano} (ex: 13.92): ")
            taxa = float(taxa_input.replace(',', '.'))
            break
        except ValueError:
            print("❌ Digite um número válido")
    
    # Calcula
    return calculadora_prefixado_por_ano(ano, taxa)

if __name__ == "__main__":
    calculadora_prefixado_por_ano(ano=int(input("digite o ano:")), taxa_anual=float(input("digite a taxa:")))