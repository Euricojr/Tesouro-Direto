import tesouro_direto_br as td

def buscar_titulo(tipo: str, ano: int):
    """
    Busca título do Tesouro Direto de um tipo específico e vencimento em um ano informado.
    Exemplo: buscar_titulo("prefixado", 2032)
    """
    print(f"🔍 BUSCANDO TESOURO {tipo.upper()} {ano}...")
    print("-" * 50)
    
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
tipo = input("Digite o tipo de título (prefixado, ipca, selic): ")
ano = int(input("Digite o ano de vencimento (ex: 2032): "))

buscar_titulo(tipo, ano)









#def buscar_tesouro_prefixado_2032():
  # """
  #  Busca especificamente o Tesouro Prefixado com vencimento em 2032
  #  """
    #print("🔍 BUSCANDO TESOURO PREFIXADO 2032...")
   # print("-" * 50)
    
   # try:
        # Busca todos os títulos
        #todos_titulos = td.busca_tesouro_direto()
        
        #print(f"✅ Total de títulos encontrados: {len(todos_titulos)}")
        
        # Procura especificamente pelo Prefixado 2032
       # titulo_encontrado = None
        
       # for index, row in todos_titulos.iterrows():
            # O index pode ser uma tupla (nome, vencimento)
          #  if isinstance(index, tuple):
               # nome_titulo = str(index[0]).lower()
               # vencimento = index[1]
                
                # Verifica se é Prefixado e se vence em 2032
               # if 'prefixado' in nome_titulo:
                  #  if hasattr(vencimento, 'year') and vencimento.year == 2032:
                  #      titulo_encontrado = (index, row)
                  #      break
                  #  elif '2032' in str(vencimento):
                  #      titulo_encontrado = (index, row)
                  #      break
        
      #  if titulo_encontrado:
          #  index, dados = titulo_encontrado
          #  print(f"🎯 TÍTULO ENCONTRADO!")#
          #  print(f"Nome: {index[0]}")
          #  print(f"Vencimento: {index[1]}")
          #  print(f"PU: R$ {dados['PU']:,.6f}")
            
         #   if 'Data Venda' in dados:
              #  print(f"Data Venda: {dados['Data Venda']}")
            
          #  return index, dados
        #else:
          #  print("❌ Tesouro Prefixado 2032 não encontrado")
          #  print("\nTítulos Prefixados disponíveis:")
            
            # Mostra todos os prefixados disponíveis
           # prefixados = []
           # for index, row in todos_titulos.iterrows():
           #     if isinstance(index, tuple):
            #        nome = str(index[0]).lower()
            #        if 'prefixado' in nome:
            #            prefixados.append((index, row))
            
            #for i, (idx, dados) in enumerate(prefixados[:10]):  # Mostra até 10
               # print(f"{i+1}. {idx[0]} - {idx[1]} - PU: R$ {dados['PU']:,.2f}")
            
           # return None, None
            
    #except Exception as e:
        #print(f"❌ Erro ao buscar título: {e}")
       # return None, None
# ---------------------------
