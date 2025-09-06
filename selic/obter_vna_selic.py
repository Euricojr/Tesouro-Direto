import pandas as pd

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