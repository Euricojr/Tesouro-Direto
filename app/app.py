import streamlit as st
import tesouro_direto_br as td
from datetime import datetime
import pandas as pd
import warnings
import requests
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Calculadora Tesouro Direto",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== FUNÇÕES TESOURO PREFIXADO ====================

def buscar_titulos_prefixados():
    """Busca TODOS os títulos Tesouro Prefixado disponíveis"""
    try:
        todos_titulos = td.busca_tesouro_direto()
        titulos_prefixados = []
        
        for index, row in todos_titulos.iterrows():
            if isinstance(index, tuple):
                nome_titulo = str(index[0]).lower()
                if 'prefixado' in nome_titulo:
                    titulos_prefixados.append((index, row))
        
        return titulos_prefixados
            
    except Exception as e:
        st.error(f"Erro ao buscar títulos: {e}")
        return []

def buscar_prefixado_por_ano(ano_vencimento):
    """Busca um Tesouro Prefixado específico por ano de vencimento"""
    try:
        titulos_prefixados = buscar_titulos_prefixados()
        
        if not titulos_prefixados:
            return None, None
        
        for index, dados in titulos_prefixados:
            vencimento = index[1]
            
            if hasattr(vencimento, 'year') and vencimento.year == ano_vencimento:
                return index, dados
            elif str(ano_vencimento) in str(vencimento):
                return index, dados
        
        return None, None
        
    except Exception as e:
        st.error(f"Erro ao buscar título: {e}")
        return None, None

def extrair_dados_prefixado_qualquer_ano(index_titulo, dados_titulo):
    """Extrai dados do título"""
    dados_extraidos = {
        'nome': index_titulo[0],
        'vencimento': index_titulo[1],
        'pu_biblioteca': float(dados_titulo['PU']),
        'valor_nominal': 1000.0,
        'data_consulta': datetime.now().date()
    }
    
    if hasattr(dados_extraidos['vencimento'], 'date'):
        dados_extraidos['vencimento'] = dados_extraidos['vencimento'].date()
    elif isinstance(dados_extraidos['vencimento'], str):
        dados_extraidos['vencimento'] = datetime.strptime(dados_extraidos['vencimento'], "%Y-%m-%d").date()
    
    return dados_extraidos

def calcular_dias_uteis(data_atual, data_vencimento):
    """Calcula dias úteis entre duas datas"""
    if isinstance(data_atual, datetime):
        data_atual = data_atual.date()
    if isinstance(data_vencimento, datetime):
        data_vencimento = data_vencimento.date()
    
    dias_corridos = (data_vencimento - data_atual).days
    dias_uteis = int(dias_corridos * (252 / 365))
    return dias_uteis, dias_corridos

def calcular_pu_prefixado_oficial(vn, taxa_anual, du):
    """Fórmula oficial do Tesouro Direto para títulos prefixados"""
    base = (taxa_anual / 100) + 1
    expoente = du / 252
    pu = vn / (base ** expoente)
    return pu

def obter_anos_disponiveis_prefixado():
    """Obtém lista dos anos disponíveis para Prefixado"""
    titulos_prefixados = buscar_titulos_prefixados()
    anos_disponiveis = set()
    
    for index, dados in titulos_prefixados:
        vencimento = index[1]
        if hasattr(vencimento, 'year'):
            anos_disponiveis.add(vencimento.year)
        elif isinstance(vencimento, str):
            try:
                ano = int(vencimento[:4])
                anos_disponiveis.add(ano)
            except:
                pass
    
    return sorted(list(anos_disponiveis))

def calculadora_prefixado_streamlit(ano, taxa_anual):
    """Versão da calculadora adaptada para Streamlit"""
    index_titulo, dados_titulo = buscar_prefixado_por_ano(ano)
    
    if index_titulo is None:
        return None
    
    dados = extrair_dados_prefixado_qualquer_ano(index_titulo, dados_titulo)
    du, dias_corridos = calcular_dias_uteis(dados['data_consulta'], dados['vencimento'])
    pu_calculado = calcular_pu_prefixado_oficial(dados['valor_nominal'], taxa_anual, du)
    
    return {
        'dados': dados,
        'dias_uteis': du,
        'dias_corridos': dias_corridos,
        'pu_calculado': pu_calculado,
        'taxa_usada': taxa_anual
    }

# ==================== FUNÇÕES TESOURO SELIC ====================

def obter_vna_selic_atual():
    """Obtém VNA atual do Tesouro Selic"""
    url = "https://brasilindicadores.com.br/titulos-publicos/vna"
    
    try:
        tabelas = pd.read_html(url)
        tabela_lft = tabelas[2]
        linha = tabela_lft.iloc[0]
        data_ref = linha["Dt. referência"]
        vna = float(str(linha["VNA"]).replace("R$", "").replace(".", "").replace(",", "."))
        return vna, data_ref
    except Exception as e:
        st.error(f"Erro ao obter VNA: {e}")
        return None, None

def calcular_vna_selic_projetado(vna_atual, taxa_selic_anual):
    """Calcula VNA projetado para D+1"""
    taxa_selic_diaria = (1 + taxa_selic_anual) ** (1/252) - 1
    vna_projetado = vna_atual * (1 + taxa_selic_diaria)
    return vna_projetado, taxa_selic_diaria

def calcular_cotacao_selic(taxa_contratada, dias_uteis):
    """Calcula cotação do Tesouro Selic"""
    expoente = dias_uteis / 252
    cotacao = 100 / ((1 + taxa_contratada) ** expoente)
    return cotacao

def calculadora_selic_streamlit(ano_vencimento, taxa_contratada, taxa_selic_projetada):
    """Calculadora do Tesouro Selic para Streamlit"""
    data_vencimento = datetime(ano_vencimento, 3, 1)
    data_compra = datetime.now()
    
    # Obter VNA
    vna_atual, data_ref = obter_vna_selic_atual()
    if vna_atual is None:
        return None
    
    # Calcular VNA projetado
    vna_projetado, taxa_diaria = calcular_vna_selic_projetado(vna_atual, taxa_selic_projetada)
    
    # Calcular dias úteis
    dias_uteis, dias_corridos = calcular_dias_uteis(data_compra, data_vencimento)
    
    # Calcular cotação e preço
    cotacao = calcular_cotacao_selic(taxa_contratada, dias_uteis)
    preco_unitario = vna_projetado * (cotacao / 100)
    
    return {
        'ano_vencimento': ano_vencimento,
        'data_vencimento': data_vencimento,
        'taxa_contratada': taxa_contratada,
        'taxa_selic': taxa_selic_projetada,
        'vna_atual': vna_atual,
        'vna_projetado': vna_projetado,
        'taxa_diaria': taxa_diaria,
        'cotacao': cotacao,
        'dias_uteis': dias_uteis,
        'dias_corridos': dias_corridos,
        'preco': preco_unitario,
        'data_ref': data_ref
    }

# ==================== FUNÇÕES TESOURO IPCA+ ====================

def calcular_vna_ipca():
    """Calcula o VNA do IPCA+ automaticamente até hoje"""
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
        r = requests.get(url, timeout=15)
        
        if r.status_code != 200:
            return usar_vna_fallback()
        
        dados = pd.DataFrame(r.json())
        dados["data"] = pd.to_datetime(dados["data"], dayfirst=True)
        dados["valor"] = dados["valor"].astype(float) / 100
        
        inicio = pd.to_datetime("2000-07-01")
        hoje = datetime.today()
        
        ipca = dados[(dados["data"] >= inicio) & (dados["data"] <= hoje)]
        
        if ipca.empty:
            return usar_vna_fallback()
        
        fator = (1 + ipca["valor"]).prod()
        vna = 1000 * fator
        
        ultima_data = ipca["data"].max()
        
        return vna, ultima_data.strftime('%m/%Y')
        
    except Exception as e:
        return usar_vna_fallback()

def usar_vna_fallback():
    """Usa um valor aproximado de VNA quando a API falha"""
    vna_estimado = 4561.46
    return vna_estimado, "10/2024 (estimado)"

def projetar_vna_ipca(vna_atual, ipca_projetado_mensal, meses=1):
    """Projeta o VNA com base no IPCA projetado"""
    vna_projetado = vna_atual * ((1 + ipca_projetado_mensal) ** meses)
    return vna_projetado

def calcular_cotacao_ipca(taxa_real_anual, dias_uteis_vencimento):
    """Calcula a cotação usando a fórmula oficial"""
    cotacao = 100 / ((1 + taxa_real_anual) ** (dias_uteis_vencimento / 252))
    return cotacao

def calculadora_ipca_streamlit(ano_vencimento, taxa_real_anual, ipca_projetado_mensal):
    """Calculadora do Tesouro IPCA+ para Streamlit"""
    # Determinar data de vencimento
    if ano_vencimento % 2 == 1:  # Ano ímpar
        data_vencimento = datetime(ano_vencimento, 5, 15)
    else:  # Ano par
        data_vencimento = datetime(ano_vencimento, 8, 15)
    
    data_compra = datetime.now()
    
    # Calcular VNA atual
    vna_atual, data_ref_vna = calcular_vna_ipca()
    
    # Calcular VNA projetado
    vna_projetado = projetar_vna_ipca(vna_atual, ipca_projetado_mensal, meses=1)
    
    # Calcular dias úteis
    dias_uteis, dias_corridos = calcular_dias_uteis(data_compra, data_vencimento)
    
    # Calcular cotação e preço
    cotacao = calcular_cotacao_ipca(taxa_real_anual, dias_uteis)
    preco_final = vna_projetado * (cotacao / 100)
    
    return {
        'ano_vencimento': ano_vencimento,
        'data_vencimento': data_vencimento,
        'taxa_real': taxa_real_anual,
        'ipca_mensal': ipca_projetado_mensal,
        'vna_atual': vna_atual,
        'vna_projetado': vna_projetado,
        'data_ref_vna': data_ref_vna,
        'cotacao': cotacao,
        'dias_uteis': dias_uteis,
        'dias_corridos': dias_corridos,
        'preco': preco_final
    }

# ==================== INTERFACE STREAMLIT ====================

def main():
    # Cabeçalho
    st.title("💰 Calculadora Tesouro Direto")
    st.markdown("### Precificação de Títulos Públicos")
    st.markdown("---")
    
    # Sidebar - Seleção do tipo de título
    st.sidebar.header("🎯 Tipo de Título")
    tipo_titulo = st.sidebar.radio(
        "Selecione o título:",
        ["Tesouro Prefixado", "Tesouro Selic", "Tesouro IPCA+"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("🎛️ Configurações")
    
    # ==================== TESOURO PREFIXADO ====================
    if tipo_titulo == "Tesouro Prefixado":
        # Buscar anos disponíveis
        with st.spinner("Buscando títulos disponíveis..."):
            anos_disponiveis = obter_anos_disponiveis_prefixado()
        
        if not anos_disponiveis:
            st.error("❌ Não foi possível carregar os títulos. Verifique sua conexão.")
            return
        
        # Inputs - texto simples
        ano_input = st.sidebar.text_input(
            "📅 Ano de vencimento:",
            value=str(anos_disponiveis[0]) if anos_disponiveis else "2029",
            help="Digite o ano (ex: 2029)"
        )
        
        taxa_input = st.sidebar.text_input(
            "📈 Taxa anual (%):",
            value="13.92",
            help="Digite a taxa anual. Ex: 13.92"
        )
        
        calcular = st.sidebar.button("🚀 Calcular", type="primary", use_container_width=True)
        
        # Layout principal
        if calcular:
            try:
                ano_selecionado = int(ano_input)
                taxa_anual = float(taxa_input.replace(',', '.'))
                
                with st.spinner("Calculando..."):
                    resultado = calculadora_prefixado_streamlit(ano_selecionado, taxa_anual)
                
                if resultado is None:
                    st.error(f"❌ Título para {ano_selecionado} não encontrado!")
                else:
                    dados = resultado['dados']
                    
                    # Resultado principal em destaque
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        st.metric(
                            label="💎 Preço Unitário (PU)",
                            value=f"R$ {resultado['pu_calculado']:,.2f}"
                        )
                    
                    with col2:
                        st.metric(
                            label="📊 Taxa Utilizada",
                            value=f"{resultado['taxa_usada']:.2f}% a.a."
                        )
                    
                    with col3:
                        st.metric(
                            label="📅 Dias Úteis",
                            value=f"{resultado['dias_uteis']} dias"
                        )
                    
                    st.markdown("---")
                    
                    # Detalhes do título
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Informações do Título")
                        st.info(f"**Título:** {dados['nome']}")
                        st.info(f"**Vencimento:** {dados['vencimento']}")
                        st.info(f"**Valor Nominal:** R$ {dados['valor_nominal']:,.2f}")
                    
                    with col2:
                        st.subheader("📅 Informações de Prazo")
                        st.success(f"**Data da Consulta:** {dados['data_consulta']}")
                        st.success(f"**Dias Corridos:** {resultado['dias_corridos']}")
                        st.success(f"**Dias Úteis:** {resultado['dias_uteis']}")
            
            except ValueError:
                st.error("❌ Por favor, insira valores numéricos válidos!")
    
    # ==================== TESOURO SELIC ====================
    elif tipo_titulo == "Tesouro Selic":
        # Inputs Selic - texto simples
        ano_input = st.sidebar.text_input(
            "📅 Ano de vencimento:",
            value="2029",
            help="Digite o ano (ex: 2029)"
        )
        
        taxa_contratada_input = st.sidebar.text_input(
            "📊 Taxa contratada (%):",
            value="0.00",
            help="Ágio (negativo) ou Deságio (positivo). Ex: -0.0291 ou 0.05"
        )
        
        taxa_selic_input = st.sidebar.text_input(
            "📈 Taxa Selic projetada (% a.a.):",
            value="11.75",
            help="Digite a taxa Selic esperada. Ex: 11.75"
        )
        
        calcular = st.sidebar.button("🚀 Calcular", type="primary", use_container_width=True)
        
        # Layout principal
        if calcular:
            try:
                ano_selecionado = int(ano_input)
                taxa_contratada = float(taxa_contratada_input.replace(',', '.'))
                taxa_selic = float(taxa_selic_input.replace(',', '.'))
                
                with st.spinner("Calculando..."):
                    resultado = calculadora_selic_streamlit(
                        ano_selecionado, 
                        taxa_contratada / 100, 
                        taxa_selic / 100
                    )
                
                if resultado is None:
                    st.error("❌ Não foi possível calcular. Verifique os dados.")
                else:
                    # Resultado principal em destaque
                    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                    
                    with col1:
                        st.metric(
                            label="💎 Preço Unitário",
                            value=f"R$ {resultado['preco']:,.2f}"
                        )
                    
                    with col2:
                        st.metric(
                            label="📊 VNA Projetado",
                            value=f"R$ {resultado['vna_projetado']:,.2f}"
                        )
                    
                    with col3:
                        st.metric(
                            label="📈 Cotação",
                            value=f"{resultado['cotacao']:.4f}%"
                        )
                    
                    with col4:
                        st.metric(
                            label="📅 Dias Úteis",
                            value=f"{resultado['dias_uteis']} dias"
                        )
                    
                    st.markdown("---")
                    
                    # Detalhes
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Informações do Título")
                        st.info(f"**Título:** Tesouro Selic {resultado['ano_vencimento']}")
                        st.info(f"**Vencimento:** {resultado['data_vencimento'].strftime('%d/%m/%Y')}")
                        st.info(f"**VNA Atual:** R$ {resultado['vna_atual']:,.2f}")
                        st.info(f"**Data Ref. VNA:** {resultado['data_ref']}")
                    
                    with col2:
                        st.subheader("📊 Análise da Taxa")
                        
                        # Análise de ágio/deságio
                        if resultado['taxa_contratada'] > 0:
                            st.warning(f"""
                            🔴 **Título com DESÁGIO** de {resultado['taxa_contratada']*100:.4f}%
                            
                            Preço MENOR que VNA  
                            R$ {resultado['preco']:,.2f} < R$ {resultado['vna_projetado']:,.2f}
                            """)
                        elif resultado['taxa_contratada'] < 0:
                            st.info(f"""
                            🟡 **Título com ÁGIO** de {abs(resultado['taxa_contratada'])*100:.4f}%
                            
                            Preço MAIOR que VNA  
                            R$ {resultado['preco']:,.2f} > R$ {resultado['vna_projetado']:,.2f}
                            """)
                        else:
                            st.success(f"""
                            🟢 **Título AO PAR** (sem ágio/deságio)
                            
                            Preço IGUAL ao VNA  
                            R$ {resultado['preco']:,.2f} = R$ {resultado['vna_projetado']:,.2f}
                            """)
                        
                        st.success(f"**Taxa Selic:** {resultado['taxa_selic']*100:.2f}% a.a.")
                        st.success(f"**Taxa Diária:** {resultado['taxa_diaria']*100:.6f}%")
                        st.success(f"**Dias Corridos:** {resultado['dias_corridos']}")
            
            except ValueError:
                st.error("❌ Por favor, insira valores numéricos válidos!")
    
    # ==================== TESOURO IPCA+ ====================
    else:
        # Inputs IPCA+ - texto simples
        ano_input = st.sidebar.text_input(
            "📅 Ano de vencimento:",
            value="2029",
            help="Digite o ano (ex: 2029, 2035, 2045)"
        )
        
        taxa_real_input = st.sidebar.text_input(
            "📊 Taxa real (% a.a.):",
            value="6.13",
            help="Digite a taxa real anual. Ex: 6.13"
        )
        
        ipca_mensal_input = st.sidebar.text_input(
            "📈 IPCA projetado mensal (%):",
            value="0.59",
            help="Digite o IPCA esperado para o próximo mês. Ex: 0.59"
        )
        
        calcular = st.sidebar.button("🚀 Calcular", type="primary", use_container_width=True)
        
        # Layout principal
        if calcular:
            try:
                ano_selecionado = int(ano_input)
                taxa_real = float(taxa_real_input.replace(',', '.'))
                ipca_mensal = float(ipca_mensal_input.replace(',', '.'))
                
                with st.spinner("Calculando..."):
                    resultado = calculadora_ipca_streamlit(
                        ano_selecionado,
                        taxa_real / 100,
                        ipca_mensal / 100
                    )
                
                if resultado is None:
                    st.error("❌ Não foi possível calcular. Verifique os dados.")
                else:
                    # Resultado principal em destaque
                    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                    
                    with col1:
                        st.metric(
                            label="💎 Preço Unitário",
                            value=f"R$ {resultado['preco']:,.2f}"
                        )
                    
                    with col2:
                        st.metric(
                            label="📊 VNA Projetado",
                            value=f"R$ {resultado['vna_projetado']:,.2f}"
                        )
                    
                    with col3:
                        st.metric(
                            label="📈 Cotação",
                            value=f"{resultado['cotacao']:.4f}%"
                        )
                    
                    with col4:
                        st.metric(
                            label="📅 Dias Úteis",
                            value=f"{resultado['dias_uteis']} dias"
                        )
                    
                    st.markdown("---")
                    
                    # Detalhes
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📋 Informações do Título")
                        st.info(f"**Título:** Tesouro IPCA+ {resultado['ano_vencimento']}")
                        st.info(f"**Vencimento:** {resultado['data_vencimento'].strftime('%d/%m/%Y')}")
                        st.info(f"**VNA Atual:** R$ {resultado['vna_atual']:,.2f}")
                        st.info(f"**Data Ref. VNA:** {resultado['data_ref_vna']}")
                    
                    with col2:
                        st.subheader("📊 Análise das Taxas")
                        st.success(f"**Taxa Real:** {resultado['taxa_real']*100:.2f}% a.a.")
                        st.success(f"**IPCA Mensal:** {resultado['ipca_mensal']*100:.2f}%")
                        st.success(f"**IPCA Anual (equiv.):** {((1 + resultado['ipca_mensal'])**12 - 1)*100:.2f}%")
                        st.success(f"**Dias Corridos:** {resultado['dias_corridos']}")
                        
                        # Taxa bruta estimada
                        taxa_bruta = (resultado['taxa_real'] + resultado['ipca_mensal'] * 12 + 
                                     resultado['taxa_real'] * resultado['ipca_mensal'] * 12)
                        st.info(f"**Taxa Bruta Estimada:** {taxa_bruta*100:.2f}% a.a.")
            
            except ValueError:
                st.error("❌ Por favor, insira valores numéricos válidos!")
    
    # ==================== INFORMAÇÕES GERAIS ====================
    st.markdown("---")
    st.subheader("📚 Informações Importantes")
    
    if tipo_titulo == "Tesouro Prefixado":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **🎯 O que é?**
            
            Título com rentabilidade definida na compra. 
            Você sabe exatamente quanto receberá.
            """)
        
        with col2:
            st.warning("""
            **⚠️ Atenção**
            
            Valores baseados na fórmula oficial. 
            Confirme sempre no Tesouro Direto.
            """)
        
        with col3:
            st.success("""
            **📖 Fórmula**
            
            PU = VN / [(Taxa/100 + 1)^(du/252)]
            
            VN = R$ 1.000
            """)
    
    elif tipo_titulo == "Tesouro Selic":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **🎯 O que é?**
            
            Título pós-fixado pela Selic. 
            Ideal para reserva de emergência.
            """)
        
        with col2:
            st.warning("""
            **⚠️ Atenção**
            
            VNA atualizado diariamente pela Selic.
            Valores são estimativas.
            """)
        
        with col3:
            st.success("""
            **📖 Fórmulas**
            
            VNA_proj = VNA × (1 + Selic_dia)
            
            Cotação = 100 / (1 + taxa)^(du/252)
            """)
    
    else:  # IPCA+
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **🎯 O que é?**
            
            Título híbrido: IPCA + taxa real.
            Proteção contra inflação.
            """)
        
        with col2:
            st.warning("""
            **⚠️ Atenção**
            
            VNA corrigido mensalmente pelo IPCA.
            Vencimentos: maio (ímpar), agosto (par).
            """)
        
        with col3:
            st.success("""
            **📖 Fórmulas**
            
            VNA_proj = VNA × (1 + IPCA_mensal)
            
            Cotação = 100 / (1 + taxa_real)^(du/252)
            
            Preço = VNA_proj × Cotação / 100
            """)

if __name__ == "__main__":
    main()