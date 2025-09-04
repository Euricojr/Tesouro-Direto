# Importa o que precisa
import tesouro_direto_br as td
from buscar_prefixados import buscar_prefixado_por_ano

# Opção 1: Direto ao ponto
index, dados = buscar_prefixado_por_ano(ano_vencimento=int(input("Digite o ano de vencimento (ex: 2032): ")))

if index:
    print(f"Encontrou: {dados['PU']}")