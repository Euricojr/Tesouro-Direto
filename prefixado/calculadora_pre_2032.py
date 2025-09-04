#import tesouro_direto_br as td

#dados = td.busca_tesouro_direto() # Busca os dados mais recentes do Tesouro Direto
#print(dados.iloc[1]) # Exibe a segunda linha do DataFrame retornado

# CALCULADORA ESPECÍFICA - TESOURO PREFIXADO 2032
# Busca, extrai dados e calcula PU para comparação

import tesouro_direto_br as td
import pandas as pd
from datetime import datetime, date
from buscador import buscar_tesouro_prefixado_2032
from extrair_dados import extrair_dados_prefixados_2032
from calcular_dias_uteis import calcular_dias_uteis
from calcular_pu_prefixado import calcular_pu_prefixado_oficial
 
def calculadora_completa_prefixado_2032():
    """
    Calculadora completa para o Tesouro Prefixado 2032
    """
    print("🚀 CALCULADORA TESOURO PREFIXADO 2032")
    print("=" * 60)
    
    # Passo 1: Buscar o título
    index_titulo, dados_titulo = buscar_tesouro_prefixado_2032()
    
    if index_titulo is None:
        print("❌ Não foi possível encontrar o título. Verifique se está disponível.")
        return
    
    # Passo 2: Extrair dados
    dados = extrair_dados_prefixados_2032(index_titulo, dados_titulo)
    
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
    
    # Passo 4: TAXA - AQUI VOCÊ PRECISA INFORMAR A TAXA REAL!
    print(f"\n⚠️  IMPORTANTE: INFORME A TAXA DO TÍTULO!")
    print("Vá no site do Tesouro Direto e veja a taxa do Prefixado 2032")
    
    # Exemplo com taxa hipotética - SUBSTITUA PELA TAXA REAL!
    taxa_exemplo = 13.92  # ← SUBSTITUA ESTA TAXA!
    
    #print(f"\n🔢 USANDO TAXA DE EXEMPLO: {taxa_exemplo}% a.a.")
    #print("(SUBSTITUA pela taxa real do site!)")
    
    # Passo 5: Calcular PU usando a fórmula oficial
    pu_calculado = calcular_pu_prefixado_oficial(
        dados['valor_nominal'], 
        taxa_exemplo, 
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

# Função auxiliar para testar com taxa específica
def testar_com_taxa_especifica(taxa_real):
    """
    Testa a calculadora com uma taxa específica que você obteve do site
    """
    print(f"\n🔄 TESTANDO COM TAXA ESPECÍFICA: {taxa_real}% a.a.")
    
    # Busca o título novamente
    index_titulo, dados_titulo = buscar_tesouro_prefixado_2032()
    
    if index_titulo:
        dados = extrair_dados_prefixados_2032(index_titulo, dados_titulo)
        du, _ = calcular_dias_uteis(dados['data_consulta'], dados['vencimento'])
        
        pu_calculado = calcular_pu_prefixado_oficial(dados['valor_nominal'], taxa_real, du)
        
        print(f"PU da Biblioteca: R$ {dados['pu_biblioteca']:,.6f}")
        print(f"PU Calculado:     R$ {pu_calculado:,.6f}")
        
        diferenca = abs(dados['pu_biblioteca'] - pu_calculado)
        print(f"Diferença:        R$ {diferenca:,.6f}")

# Execute a calculadora
if __name__ == "__main__":
    calculadora_completa_prefixado_2032()
    
    print(f"\n" + "="*60)
    print("PRÓXIMOS PASSOS:")
    print("1. Execute o código acima")
    print("2. Vá no site do Tesouro Direto")
    print("3. Encontre a taxa do Prefixado 2032")
    print("4. Execute: testar_com_taxa_especifica(TAXA_REAL)")
    print("="*60)
