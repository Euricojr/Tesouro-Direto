import requests
import pandas as pd
from datetime import datetime, timedelta




def calcular_vna_selic_projetado(vna_atual, taxa_selic_anual):
    """
    Calcula VNA projetado para D+1 (liquidação)
    VNA_projetado = VNA_atual × (1 + taxa_selic_diaria)
    """
    # Converter taxa anual para diária
    taxa_selic_diaria = (1 + taxa_selic_anual) ** (1/252) - 1
    
    vna_projetado = vna_atual * (1 + taxa_selic_diaria)
    
    print(f"Taxa Selic anual: {taxa_selic_anual*100:.2f}%")
    print(f"Taxa Selic diária: {taxa_selic_diaria*100:.6f}%")
    print(f"VNA atual: R$ {vna_atual:,.2f}")
    print(f"VNA projetado (D+1): R$ {vna_projetado:,.2f}")
    
    return vna_projetado

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

def calcular_dias_uteis(data_atual, data_vencimento):
    """
    Calcula dias úteis entre duas datas (aproximação usando 252 dias úteis/ano)
    """
    dias_corridos = (data_vencimento - data_atual).days
    dias_uteis = int(dias_corridos * (252 / 365))
    return dias_uteis, dias_corridos


def obter_vna_selic_atual():
    url = "https://brasilindicadores.com.br/titulos-publicos/vna"

    try:
        # Lê todas as tabelas da página
        tabelas = pd.read_html(url)
       

        # A tabela da LFT (Tesouro Selic) normalmente é a terceira (índice 2)
        tabela_lft = tabelas[2]

        # Extrair linha da LFT
        linha = tabela_lft.iloc[0]  
        data_ref = linha["Dt. referência"]
        vna = float(str(linha["VNA"]).replace("R$", "").replace(".", "").replace(",", "."))

        return vna, data_ref
    
    except Exception as e:
        print(f"Erro ao obter VNA alternativo: {e}")
        return None, None
if __name__ == "__main__":
    vna, data = obter_vna_selic_atual()
    print(vna)



def calculadora_tesouro_selic(ano_vencimento, taxa_contratada=0.0, taxa_selic_projetada=None):
    """
    Calculadora do Tesouro Selic (LFT) baseada no documento oficial
    
    Args:
        ano_vencimento (int): Ano de vencimento
        taxa_contratada (float): Taxa de ágio/deságio (decimal, ex: -0.0001 para -0.01%)
        taxa_selic_projetada (float): Taxa Selic projetada anual (se None, pede input)
    """
    print("🚀 CALCULADORA TESOURO SELIC (LFT)")
    print("=" * 50)
    
    # Data de vencimento (Tesouro Selic geralmente vence em março)
    data_vencimento = datetime(ano_vencimento, 3, 1)  # 1º de março
    data_compra = datetime.now()
    
    print(f"📅 Data compra: {data_compra.strftime('%d/%m/%Y')}")
    print(f"📅 Data vencimento: {data_vencimento.strftime('%d/%m/%Y')}")
    print(f"📊 Taxa contratada: {taxa_contratada*100:.4f}% a.a.")
    
    # Obter taxa Selic se não fornecida
    if taxa_selic_projetada is None:
        while True:
            try:
                selic_input = input("Taxa Selic projetada (ex: 11.75): ")
                taxa_selic_projetada = float(selic_input.replace(',', '.')) / 100
                break
            except ValueError:
                print("Digite um número válido!")
    
    print(f"📈 Taxa Selic projetada: {taxa_selic_projetada*100:.2f}% a.a.")
    
    # PASSO 1: Obter VNA atual
    print(f"\n🔄 PASSO 1: Obtendo VNA atual...")
    
    vna_atual, data_ref = obter_vna_selic_atual(  )
    

    
    # PASSO 2: Calcular VNA projetado
    print(f"\n🔄 PASSO 2: Calculando VNA projetado...")
    vna_projetado = calcular_vna_selic_projetado(vna_atual, taxa_selic_projetada)
    
    # PASSO 3: Calcular dias úteis
    print(f"\n🔄 PASSO 3: Calculando prazo...")
    dias_uteis, dias_corridos = calcular_dias_uteis(data_compra, data_vencimento)
    print(f"✅ Dias corridos: {dias_corridos}")
    print(f"✅ Dias úteis (aproximado): {dias_uteis}")
    
    # PASSO 4: Calcular cotação
    print(f"\n🔄 PASSO 4: Calculando cotação...")
    cotacao = calcular_cotacao_selic(taxa_contratada, dias_uteis)
    print(f"✅ Cotação: {cotacao:.4f}%")
    
    # PASSO 5: Calcular preço
    print(f"\n🔄 PASSO 5: Calculando preço...")
    preco_unitario = vna_projetado * (cotacao / 100)
    print(f"✅ PREÇO UNITÁRIO: R$ {preco_unitario:,.2f}")
    
    # Análise da taxa
    print(f"\n📊 ANÁLISE:")
    print("-" * 30)
    if taxa_contratada > 0:
        print(f"🔴 Título com DESÁGIO de {taxa_contratada*100:.4f}%")
        print(f"    Preço MENOR que VNA (R$ {preco_unitario:,.2f} < R$ {vna_projetado:,.2f})")
    elif taxa_contratada < 0:
        print(f"🟡 Título com ÁGIO de {abs(taxa_contratada)*100:.4f}%")
        print(f"    Preço MAIOR que VNA (R$ {preco_unitario:,.2f} > R$ {vna_projetado:,.2f})")
    else:
        print(f"🟢 Título AO PAR (sem ágio/deságio)")
        print(f"    Preço IGUAL ao VNA (R$ {preco_unitario:,.2f} = R$ {vna_projetado:,.2f})")
    
    # Resumo final
    print(f"\n📋 RESUMO FINAL:")
    print("-" * 40)
    print(f"Título: Tesouro Selic {ano_vencimento}")
    print(f"VNA projetado: R$ {vna_projetado:,.2f}")
    print(f"Cotação: {cotacao:.4f}%")
    print(f"🎯 PREÇO: R$ {preco_unitario:,.2f}")
    print(f"💰 Rentabilidade: Taxa Selic {taxa_contratada*100:+.4f}% a.a.")
    
    return {
        'ano_vencimento': ano_vencimento,
        'data_vencimento': data_vencimento,
        'taxa_contratada': taxa_contratada,
        'taxa_selic': taxa_selic_projetada,
        'vna_projetado': vna_projetado,
        'cotacao': cotacao,
        'dias_uteis': dias_uteis,
        'preco': preco_unitario
    }

def calculadora_selic_interativa():
    """
    Versão interativa da calculadora
    """
    print("🎯 CALCULADORA INTERATIVA - TESOURO SELIC")
    print("=" * 45)

    # Ano de vencimento
    while True:
        try:
            ano = int(input("📅 Ano de vencimento (ex: 2026): "))
            if ano <= datetime.now().year:
                print("❌ Ano deve ser futuro!")
                continue
            break
        except ValueError:
            print("❌ Digite um número válido")
    
    # Taxa contratada
    while True:
        try:
            taxa_input = input("📊 Taxa contratada % (Enter para 0.00%): ").strip()
            if not taxa_input:
                taxa = 0.0
            else:
                taxa = float(taxa_input.replace(',', '.')) / 100
            break
        except ValueError:
            print("❌ Digite um número válido")
    
    return calculadora_tesouro_selic(ano, taxa)

if __name__ == "__main__":
    vna, data = obter_vna_selic_atual()
    print("✅ VNA Selic:", vna, "Data ref:", data)
    
    calculadora_selic_interativa()