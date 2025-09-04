def calcular_pu_prefixado_oficial(vn, taxa_anual, du):
    """
    Fórmula oficial do Tesouro Direto para títulos prefixados:
    PU = VN / [(Taxa/100 + 1)^(du/252)]
    """
    base = (taxa_anual / 100) + 1
    expoente = du / 252
    pu = vn / (base ** expoente)
    return pu