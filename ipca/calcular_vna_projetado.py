from calculadora_ipca import calcular_vna

ipca_projetado_mensal = 0.56 / 100  # 0,56% ao mês convertido para decimal

def vna_projetado_ipca(vna_atual, ipca_projetado_mensal):
    vna_projetado = vna_atual * (1 + ipca_projetado_mensal)
    return vna_projetado

# Aqui você precisa chamar a função calcular_vna() para obter o número
vna_atual = calcular_vna()

vna_projetado = vna_projetado_ipca(vna_atual, ipca_projetado_mensal)
#print(vna_projetado)
