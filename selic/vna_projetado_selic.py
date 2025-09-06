def calcular_vna_selic_projetado(vna_atual, taxa_selic_anual):
    """
    Calcula VNA projetado para D+1 (liquidação)
    VNA_projetado = VNA_atual × (1 + taxa_selic_diaria)
    """
    # Converter taxa anual para diária
    taxa_selic_diaria = (1 + taxa_selic_anual) ** (1/252) - 1
    
    vna_projetado = vna_atual * (1 + taxa_selic_diaria)
    
    print(f"Taxa Selic anual: {taxa_selic_anual*100:.2f}%")
    print(f"Taxa Selic diária: {taxa_selic_diaria*100:.6f}%")
    print(f"VNA atual: R$ {vna_atual:,.2f}")
    print(f"VNA projetado (D+1): R$ {vna_projetado:,.2f}")
    
    return vna_projetado
