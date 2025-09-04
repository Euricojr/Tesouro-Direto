import tesouro_direto_br as td


def buscar_tesouro_prefixado(ano):  # olhar qual é o ano e a partir disso criar a função para calcular os anos diferentes
    """
    Busca especificamente o Tesouro Prefixado com vencimento em 2032
    """
    print("🔍 BUSCANDO TESOURO PREFIXADO 2032...")
    print("-" * 50)

    try:
        # Busca todos os títulos
        todos_titulos = td.busca_tesouro_direto()
        
        print(f"✅ Total de títulos encontrados: {len(todos_titulos)}")
        
        # Procura especificamente pelo Prefixado 2032
        titulo_encontrado = ("prefixado",{ano})
        
        for index, row in todos_titulos.iterrows():
            # O index pode ser uma tupla (nome, vencimento)
            if isinstance(index, tuple):
                nome_titulo = str(index[0]).lower()
                vencimento = index[1]
                
                # Verifica se é Prefixado e se vence em 2032
                if 'prefixado' in nome_titulo:
                    if hasattr(vencimento, 'year') and vencimento.year == ano:
                        titulo_encontrado = (index, row)
                        break
                    elif '2032' in str(vencimento):
                        titulo_encontrado = (index, row)
                        break
        
        if titulo_encontrado:
            index, dados = titulo_encontrado
            print(f"🎯 TÍTULO ENCONTRADO!")
            print(f"Nome: {index[0]}")
            print(f"Vencimento: {index[1]}")
            print(f"PU: R$ {dados['PU']:,.6f}")
            
            if 'Data Venda' in dados:
                print(f"Data Venda: {dados['Data Venda']}")
            
            return index, dados
        else:
            print("❌ Tesouro Prefixado 2032 não encontrado")
            print("\nTítulos Prefixados disponíveis:")
            
            # Mostra todos os prefixados disponíveis
            prefixados = []
            for index, row in todos_titulos.iterrows():
                if isinstance(index, tuple):
                    nome = str(index[0]).lower()
                    if 'prefixado' in nome:
                        prefixados.append((index, row))
            
            for i, (idx, dados) in enumerate(prefixados[:10]):  # Mostra até 10
                print(f"{i+1}. {idx[0]} - {idx[1]} - PU: R$ {dados['PU']:,.2f}")
            
            return None, None
            
    except Exception as e:
        print(f"❌ Erro ao buscar título: {e}")
        return None, None

