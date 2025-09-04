import tesouro_direto_br as td

def buscar_taxa_titulo(tipo: str, ano: int):
    """
    Busca taxa de compra/venda de um título do Tesouro Direto
    Exemplo: buscar_taxa_titulo("ipca", 2035)
    """
    print(f"🔍 BUSCANDO TAXA {tipo.upper()} {ano}...")
    print("-" * 50)

    try:
        # Busca os títulos pela API
        titulos_taxa = td.busca_tesouro_direto("taxa")
        print(f"✅ Total de títulos encontrados: {len(titulos_taxa)}")

        titulo_encontrado = None

        for index, row in titulos_taxa.iterrows():
            if isinstance(index, tuple):
                nome_titulo = str(index[0]).lower()
                vencimento = index[1]

                # Confere se o tipo está no nome
                if tipo.lower() in nome_titulo:
                    # Checa se o vencimento bate
                    if hasattr(vencimento, "year") and vencimento.year == ano:
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
            print(f"Taxa Compra: {dados['Taxa Compra Manha']:.4f}%")
            print(f"Taxa Venda: {dados['Taxa Venda Manha']:.4f}%")
            return index, dados
        else:
            print(f"❌ Tesouro {tipo} {ano} não encontrado")
            return None, None

    except Exception as e:
        print(f"❌ Erro ao buscar taxa: {e}")
        return None, None
tipo = input("Digite o tipo de título (prefixado, ipca, selic): ")
ano = int(input("Digite o ano de vencimento (ex: 2032): "))

buscar_taxa_titulo(tipo, ano)

