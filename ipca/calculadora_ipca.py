import requests
import pandas as pd
from datetime import datetime, timedelta
from calculadora_vna_ipca import calcular_vna
from calcular_dias_uteis import calcular_dias_uteis
from função_obter_ultimo_dia_15 import obter_ultimo_dia_15
from calcular_vna_projetado_ipca import calcular_vna_projetado



def calcular_cotacao(taxa_real_anual, dias_uteis_vencimento):
    """
    Calcula a cotação usando a fórmula:
    Cotação (%) = 100 / (1 + taxa_real)^(dias_úteis / 252)
    """
    cotacao = 100 / ((1 + taxa_real_anual) ** (dias_uteis_vencimento / 252))
    return cotacao

def calculadora_ipca_simples(ano_vencimento, taxa_real_anual, ipca_projetado_mensal=None):
    """
    Calculadora simples do Tesouro IPCA+
    
    Args:
        ano_vencimento (int): Ano de vencimento (ex: 2029)
        taxa_real_anual (float): Taxa real anual em decimal (ex: 0.0613 para 6.13%)
        ipca_projetado_mensal (float): IPCA projetado mensal (padrão 0.5%)
    """
    if ipca_projetado_mensal is None:
        while True:
            try:
                ipca_input = input('IPCA projetado mensal (ex: 0.0059 para 0,59%): ')
                ipca_projetado_mensal = float(ipca_input.replace(',', '.'))
                break
            except ValueError:
                print("Digite um número válido!")

    print(f"🚀 CALCULADORA TESOURO IPCA+ {ano_vencimento}")
    print("=" * 60)
    
    # Determinar data de vencimento (regra: maio para ímpar, agosto para par)
    if ano_vencimento % 2 == 1:  # Ano ímpar
        data_vencimento = datetime(ano_vencimento, 5, 15)
        print(f"📅 Vencimento: 15/05/{ano_vencimento} (ano ímpar)")
    else:  # Ano par
        data_vencimento = datetime(ano_vencimento, 8, 15)
        print(f"📅 Vencimento: 15/08/{ano_vencimento} (ano par)")
    
    data_compra = datetime.now()
    print(f"📅 Data de compra: {data_compra.strftime('%d/%m/%Y')}")
    print(f"📊 Taxa real: {taxa_real_anual*100:.2f}% a.a.")
    print(f"📈 IPCA projetado mensal: {ipca_projetado_mensal*100:.2f}%")
    
    # Passo 1: Calcular VNA atual (referência)
    print(f"\n🔄 PASSO 1: Calculando VNA atual...")
    vna_atual = calcular_vna()
    if vna_atual is None:
        return None
    print(f"✅ VNA atual: R$ {vna_atual:,.2f}")
    
    # Passo 2: Calcular VNA projetado
    print(f"\n🔄 PASSO 2: Calculando VNA projetado...")
    vna_projetado = calcular_vna_projetado(data_compra, ipca_projetado_mensal)
    if vna_projetado is None:
        return None
    print(f"✅ VNA projetado: R$ {vna_projetado:,.2f}")
    
    # Passo 3: Calcular dias úteis
    print(f"\n🔄 PASSO 3: Calculando prazo...")
    dias_uteis, dias_corridos = calcular_dias_uteis(data_compra, data_vencimento)
    print(f"✅ Dias corridos: {dias_corridos}")
    print(f"✅ Dias úteis: {dias_uteis}")
    
    # Passo 4: Calcular cotação
    print(f"\n🔄 PASSO 4: Calculando cotação...")
    cotacao = calcular_cotacao(taxa_real_anual, dias_uteis)
    print(f"✅ Cotação: {cotacao:.4f}%")
    
    # Passo 5: Calcular preço final
    print(f"\n🔄 PASSO 5: Calculando preço final...")
    preco_final = vna_projetado * (cotacao / 100)
    print(f"✅ PREÇO DO TÍTULO: R$ {preco_final:,.2f}")
    
    # Resumo
    print(f"\n📊 RESUMO FINAL:")
    print("-" * 40)
    print(f"Título: Tesouro IPCA+ {ano_vencimento}")
    print(f"Vencimento: {data_vencimento.strftime('%d/%m/%Y')}")
    print(f"Taxa real: {taxa_real_anual*100:.2f}% a.a.")
    print(f"VNA projetado: R$ {vna_projetado:,.2f}")
    print(f"Cotação: {cotacao:.4f}%")
    print(f"🎯 PREÇO: R$ {preco_final:,.2f}")
    
    return {
        'ano_vencimento': ano_vencimento,
        'data_vencimento': data_vencimento,
        'taxa_real': taxa_real_anual,
        'vna_projetado': vna_projetado,
        'cotacao': cotacao,
        'dias_uteis': dias_uteis,
        'preco': preco_final
    }

#def calculadora_ipca_interativa():
    """
    Versão interativa - pede os dados pro usuário
    """
    print("🎯 CALCULADORA INTERATIVA - TESOURO IPCA+")
    print("=" * 50)
    
    # Pede o ano
    while True:
        try:
            ano = int(input("📅 Digite o ano de vencimento (ex: 2029): "))
            if ano < datetime.now().year:
                print("❌ O ano deve ser futuro!")
                continue
            break
        except ValueError:
            print("❌ Digite um número válido")
    
    # Pede a taxa
    while True:
        try:
            taxa_input = input(f"📊 Digite a taxa real do IPCA+ {ano} (ex: 6.13): ")
            taxa = float(taxa_input.replace(',', '.')) / 100  # Converte para decimal
            break
        except ValueError:
            print("❌ Digite um número válido (ex: 6.13)")
    
    # IPCA projetado (opcional)
    while True:
        try:
            ipca_input = input("📈 IPCA projetado mensal em % (Enter para 0.5%): ").strip()
            if not ipca_input:
                ipca_mensal = 0.0059  # Padrão 0.5%
            else:
                ipca_mensal = float(ipca_input.replace(',', '.')) / 100
            break
        except ValueError:
            print("❌ Digite um número válido")
    
    # Calcula
    return calculadora_ipca_simples(ano, taxa, ipca_mensal)

if __name__ == "__main__":
    # Versão rápida com inputs diretos
    ano = int(input("📅 Digite o ano de vencimento: "))
    taxa = float(input("📊 Digite a taxa real (ex: 6.13): ")) / 100
 
    
    calculadora_ipca_simples(ano, taxa)