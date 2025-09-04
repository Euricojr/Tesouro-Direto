import tesouro_direto_br as td

todos_titulos = td.busca_tesouro_direto()
print(f"✅ Total de títulos encontrados: {len(todos_titulos)}")

#titulo_encontrado = input("Digite o nome do título que deseja buscar: ").strip().lower()
#print(f"🔍 BUSCANDO TESOURO {titulo_encontrado.upper()}...")
#print(titulo_encontrado)

#dados = td.busca_tesouro_direto(tipo="venda") # Busca os dados mais recentes do Tesouro Direto
#print(dados.iloc[12]) # Exibe a segunda linha do DataFrame retornado
#import tesouro_direto_br as td

def buscar_titulo(tipo: str, ano: int):
    """
    Busca título do Tesouro Direto de um tipo específico e vencimento em um ano informado.
    Exemplo: buscar_titulo("prefixado", 2032)
    """
    #print(f"🔍 BUSCANDO TESOURO {tipo.upper()} {ano}...")
    #print("-" * 50)
    
    try:
        # Busca todos os títulos
        todos_titulos = td.busca_tesouro_direto()
        print(f"✅ Total de títulos encontrados: {len(todos_titulos)}")

        titulo_encontrado = None

        for index, row in todos_titulos.iterrows():
            if isinstance(index, tuple):
                nome_titulo = str(index[0]).lower()
                vencimento = index[1]

                # Confere se o tipo está no nome
                if tipo.lower() in nome_titulo:
                    # Checa se o vencimento bate com o ano informado
                    if hasattr(vencimento, 'year') and vencimento.year == ano:
                        titulo_encontrado = (index, row)
                        break
                    elif str(ano) in str(vencimento):
                        titulo_encontrado = (index, row)
                        break

        if titulo_encontrado:
            index, dados = titulo_encontrado
            print("🎯 TÍTULO ENCONTRADO!")
            print(f"Nome: {index[0]}")
            print(f"Vencimento: {index[1]}")
            print(f"PU: R$ {dados['PU']:,.6f}")
            if 'Data Venda' in dados:
                print(f"Data Venda: {dados['Data Venda']}")
            return index, dados
        else:
            print(f"❌ Tesouro {tipo} {ano} não encontrado")
            print("\nTítulos disponíveis do tipo escolhido:")
            
            prefixados = []
            for index, row in todos_titulos.iterrows():
                if isinstance(index, tuple):
                    nome = str(index[0]).lower()
                    if tipo.lower() in nome:
                        prefixados.append((index, row))
            
            for i, (idx, dados) in enumerate(prefixados[:10]):  # mostra só os 10 primeiros
                print(f"{i+1}. {idx[0]} - {idx[1]} - PU: R$ {dados['PU']:,.2f}")

            return None, None

    except Exception as e:
        print(f"❌ Erro ao buscar título: {e}")
        return None, None


# ---------------------------
# Uso interativo:
#tipo = input("Digite o tipo de título (prefixado, ipca, selic): ")
#ano = int(input("Digite o ano de vencimento (ex: 2032): "))

#buscar_titulo(tipo, ano)



import requests
import pandas as pd
from datetime import datetime

def calcular_vna():
    """
    Calcula o VNA (Valor Nominal Atualizado) automaticamente até hoje.
    Base: R$ 1.000,00 em 15/07/2000 corrigido pelo IPCA.
    """
    # Série 433 = IPCA (variação % mensal) no SGS do Bacen
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
    r = requests.get(url)
    dados = pd.DataFrame(r.json())
    
    # Preparar os dados
    dados["data"] = pd.to_datetime(dados["data"], dayfirst=True)
    dados["valor"] = dados["valor"].astype(float) / 100  # converte % para fração
    
    # Intervalo: de jul/2000 até hoje
    inicio = pd.to_datetime("2000-07-01")
    hoje = datetime.today()
    
    ipca = dados[(dados["data"] >= inicio) & (dados["data"] <= hoje)]
    
    # Calcula o fator acumulado
    fator = (1 + ipca["valor"]).prod()
    vna = 1000 * fator
    
    return vna

# -------------------------------
vna_hoje = calcular_vna()
print(f"📊 VNA atualizado em {datetime.today().date()}: R$ {vna_hoje:,.2f}")
