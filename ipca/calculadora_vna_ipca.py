import requests
import pandas as pd
from datetime import datetime


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


# IMPORTANTE: NÃO executar durante o import!
# Comentado para evitar erro ao importar em outros scripts
# vna_hoje = calcular_vna()


#if __name__ == "__main__":
    # Testes do módulo
    print("🧪 TESTE DO MÓDULO CALCULADORA VNA")
    print("="*60)
    
    # Teste 1: Calcular VNA atual
    print("\n📊 Teste 1: VNA Atual")
    print("-"*60)
    vna = calcular_vna(debug=False)
    
    if vna:
        print(f"\n✅ VNA em {datetime.today().strftime('%d/%m/%Y')}: R$ {vna:,.2f}")
    else:
        print("\n❌ Falha ao calcular VNA")
    
    # Teste 2: Ver histórico (últimos 12 meses)
    print("\n\n📈 Teste 2: Histórico Recente")
    print("-"*60)
    historico = obter_historico_vna()
    if historico is not None and not historico.empty:
        print("\nÚltimos 12 meses:")
        print(historico.tail(12).to_string(index=False))
    
    print("\n" + "="*60)
    print("✅ Testes concluídos!")