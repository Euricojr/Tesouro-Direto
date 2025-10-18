import requests
import pandas as pd
from datetime import datetime, timedelta



def calcular_vna(debug=False):
    """
    Calcula o VNA (Valor Nominal Atualizado) automaticamente até hoje.
    Base: R$ 1.000,00 em 15/07/2000 corrigido pelo IPCA.
    
    Args:
        debug (bool): Se True, mostra os dados completos
    
    Returns:
        float: VNA calculado ou None se houver erro
    """
    try:
        # Série 433 = IPCA (variação % mensal) no SGS do Bacen
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
        
        print("🔄 Buscando dados do IPCA na API do BCB...")
        r = requests.get(url, timeout=15)
        
        # Verificar resposta
        if r.status_code != 200:
            print(f"⚠️  API retornou status {r.status_code}")
            return usar_vna_fallback()
        
        if not r.text or r.text.strip() == '':
            print("⚠️  API retornou resposta vazia")
            return usar_vna_fallback()
        
        # Processar dados
        dados = pd.DataFrame(r.json())
        
        if dados.empty:
            print("⚠️  Nenhum dado retornado")
            return usar_vna_fallback()
        
        # Preparar os dados
        dados["data"] = pd.to_datetime(dados["data"], dayfirst=True)
        dados["valor"] = dados["valor"].astype(float) / 100  # converte % para fração
        
        # Intervalo: de jul/2000 até hoje
        inicio = pd.to_datetime("2000-07-01")
        hoje = datetime.today()
        
        ipca = dados[(dados["data"] >= inicio) & (dados["data"] <= hoje)]
        
        if ipca.empty:
            print("⚠️  Nenhum dado no período")
            return usar_vna_fallback()
        
        # Calcula o fator acumulado
        fator = (1 + ipca["valor"]).prod()
        vna = 1000 * fator
        
        # Info sobre o cálculo
        ultima_data = ipca["data"].max()
        qtd_meses = len(ipca)
        
        print(f"✅ VNA calculado: R$ {vna:,.2f}")
        print(f"   📅 Base: 01/07/2000 (R$ 1.000,00)")
        print(f"   📈 Meses de IPCA: {qtd_meses}")
        print(f"   📊 Último IPCA: {ultima_data.strftime('%m/%Y')}")
        print(f"   🔢 Fator acumulado: {fator:.6f}")
        
        # Debug: mostrar tabela completa
        if debug:
            print("\n" + "="*60)
            print("DADOS COMPLETOS DO IPCA:")
            print("="*60)
            print(ipca.tail(12))  # Últimos 12 meses
        
        return vna
        
    except requests.exceptions.Timeout:
        print("⚠️  Timeout ao conectar na API do BCB")
        return usar_vna_fallback()
    
    except requests.exceptions.ConnectionError:
        print("⚠️  Erro de conexão com a API do BCB")
        return usar_vna_fallback()
    
    except requests.exceptions.JSONDecodeError:
        print("⚠️  API não retornou JSON válido")
        print(f"Resposta: {r.text[:200]}...")
        return usar_vna_fallback()
    
    except KeyError as e:
        print(f"⚠️  Campo ausente nos dados: {e}")
        return usar_vna_fallback()
    
    except Exception as e:
        print(f"⚠️  Erro inesperado: {type(e).__name__}: {str(e)}")
        return usar_vna_fallback()


def usar_vna_fallback():
    """
    Usa um valor aproximado de VNA quando a API falha
    Atualizado em outubro/2024
    """
    vna_estimado = 4561.46
    
    print("\n" + "="*60)
    print("⚠️  MODO FALLBACK ATIVADO")
    print("="*60)
    print(f"📊 Usando VNA estimado: R$ {vna_estimado:,.2f}")
    print("⚠️  Este é um valor aproximado de outubro/2024!")
    print("⚠️  Para valores exatos, verifique:")
    print("    https://www.tesourodireto.com.br")
    print("="*60 + "\n")
    
    return vna_estimado


def obter_historico_vna(ano_inicio=2000, mes_inicio=7):
    """
    Retorna histórico completo do VNA mês a mês
    
    Args:
        ano_inicio (int): Ano inicial (padrão: 2000)
        mes_inicio (int): Mês inicial (padrão: 7 = julho)
    
    Returns:
        DataFrame: Histórico com data, IPCA e VNA acumulado
    """
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
        r = requests.get(url, timeout=15)
        dados = pd.DataFrame(r.json())
        
        dados["data"] = pd.to_datetime(dados["data"], dayfirst=True)
        dados["ipca_pct"] = dados["valor"].astype(float)
        dados["ipca_decimal"] = dados["ipca_pct"] / 100
        
        inicio = pd.to_datetime(f"{ano_inicio}-{mes_inicio:02d}-01")
        dados = dados[dados["data"] >= inicio].copy()
        
        # Calcular VNA acumulado mês a mês
        dados["fator"] = 1 + dados["ipca_decimal"]
        dados["vna"] = (dados["fator"].cumprod() * 1000).round(2)
        
        return dados[["data", "ipca_pct", "vna"]]
        
    except Exception as e:
        print(f"Erro ao obter histórico: {e}")
        return None

def calcular_dias_uteis(data_atual, data_vencimento):
    """
    Calcula dias úteis entre duas datas (aproximação usando 252 dias úteis/ano)
    """
    dias_corridos = (data_vencimento - data_atual).days
    dias_uteis = int(dias_corridos * (252 / 365))
    return dias_uteis, dias_corridos


def projetar_vna(vna_atual, ipca_projetado_mensal, meses=1):
    """
    Projeta o VNA com base no IPCA projetado
    """
    vna_projetado = vna_atual * ((1 + ipca_projetado_mensal) ** meses)
    return vna_projetado


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
        ipca_projetado_mensal (float): IPCA projetado mensal em decimal (ex: 0.0059 para 0.59%)
    """
    if ipca_projetado_mensal is None:
        while True:
            try:
                ipca_input = input('📈 IPCA projetado mensal (ex: 0.59 para 0.59%): ')
                ipca_projetado_mensal = float(ipca_input.replace(',', '.')) / 100
                break
            except ValueError:
                print("⚠️  Digite um número válido!")

    print(f"\n🚀 CALCULADORA TESOURO IPCA+ {ano_vencimento}")
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
    
    # Passo 1: Calcular VNA atual
    print(f"\n🔄 PASSO 1: Calculando VNA atual...")
    vna_atual = calcular_vna()
    if vna_atual is None:
        print("❌ Erro ao calcular VNA atual")
        return None
    print(f"✅ VNA atual: R$ {vna_atual:,.2f}")
    
    # Passo 2: Calcular VNA projetado
    print(f"\n🔄 PASSO 2: Calculando VNA projetado...")
    # Calcular quantos meses até o vencimento para projeção
    meses_ate_vencimento = ((data_vencimento.year - data_compra.year) * 12 + 
                            (data_vencimento.month - data_compra.month))
    vna_projetado = projetar_vna(vna_atual, ipca_projetado_mensal, meses=1)
    print(f"✅ VNA projetado (1 mês): R$ {vna_projetado:,.2f}")
    
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
        'vna_atual': vna_atual,
        'vna_projetado': vna_projetado,
        'cotacao': cotacao,
        'dias_uteis': dias_uteis,
        'preco': preco_final
    }


if __name__ == "__main__":
    print("💰 CALCULADORA DE PU - TESOURO IPCA+")
    print("=" * 60)
    
    # Inputs do usuário
    ano = int(input("\n📅 Digite o ano de vencimento (ex: 2029): "))
    taxa = float(input("📊 Digite a taxa real % a.a. (ex: 6.13): ")) / 100
    
    # Executar calculadora
    resultado = calculadora_ipca_simples(ano, taxa)
    
    if resultado:
        print("\n✅ Cálculo concluído com sucesso!")