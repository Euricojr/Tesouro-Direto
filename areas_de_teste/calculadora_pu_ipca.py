from datetime import date
from ipca.calculadora_vna_ipca import vna_hoje
def preco_ipca(vna, taxa_real, vencimento, hoje=date.today(),):
    """
    Calcula o preço teórico (PU) de um Tesouro IPCA+ Principal.
    
    vna        -> Valor Nominal Atualizado (corrigido pelo IPCA até hoje)
    taxa_real  -> taxa real anual (ex: 0.06 = 6% a.a.)
    vencimento -> data de vencimento do título (objeto datetime.date)
    hoje       -> data de cálculo (default: hoje)
    """
    # diferença em dias corridos
    dias = (vencimento - hoje).days
    
    # converte para anos (base 252 úteis ou 365 corridos; simplificando: 252 úteis)
    t = dias / 252  
    
    # valor presente
    pu = vna / ((1 + taxa_real) ** t)
    print(dias)
    print(t)
    return pu

# -------------------------------
# Exemplo
vna_hoje = vna_hoje       # exemplo do VNA que você já calculouS
taxa_real = 0.0731        # 6% a.a.
vencimento = date(2040,8,15)

pu = preco_ipca(vna_hoje, taxa_real, vencimento)
#print(f"📊 PU teórico: R$ {pu:,.2f}")
