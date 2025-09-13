import streamlit as st
import tesouro_direto_br as td
from datetime import datetime
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Calculadora Tesouro Prefixado",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SUAS FUNÇÕES ORIGINAIS ====================

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
    dias_corridos = (data_vencimento - data_atual).days
    dias_uteis = int(dias_corridos * (252 / 365))
    return dias_uteis, dias_corridos

def calcular_pu_prefixado_oficial(vn, taxa_anual, du):
    """Fórmula oficial do Tesouro Direto para títulos prefixados"""
    base = (taxa_anual / 100) + 1
    expoente = du / 252
    pu = vn / (base ** expoente)
    return pu

def obter_anos_disponiveis():
    """Obtém lista dos anos disponíveis"""
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
    # Buscar o título
    index_titulo, dados_titulo = buscar_prefixado_por_ano(ano)
    
    if index_titulo is None:
        return None
    
    # Extrair dados
    dados = extrair_dados_prefixado_qualquer_ano(index_titulo, dados_titulo)
    
    # Calcular dias úteis
    du, dias_corridos = calcular_dias_uteis(dados['data_consulta'], dados['vencimento'])
    
    # Calcular PU
    pu_calculado = calcular_pu_prefixado_oficial(dados['valor_nominal'], taxa_anual, du)
    
    return {
        'dados': dados,
        'dias_uteis': du,
        'dias_corridos': dias_corridos,
        'pu_calculado': pu_calculado,
        'taxa_usada': taxa_anual
    }

# ==================== INTERFACE STREAMLIT ====================

def main():
    # Título principal
    st.title("💰 Calculadora Tesouro Prefixado")
    st.markdown("---")
    
    # Sidebar com controles
    st.sidebar.header("🎛️ Configurações")
    
    # Buscar anos disponíveis
    with st.spinner("Buscando títulos disponíveis..."):
        anos_disponiveis = obter_anos_disponiveis()
    
    if not anos_disponiveis:
        st.error("❌ Não foi possível carregar os títulos. Verifique sua conexão.")
        return
    
    # Seleção do ano
    ano_selecionado = st.sidebar.selectbox(
        "📅 Selecione o ano de vencimento:",
        anos_disponiveis,
        index=0
    )
    
    with st.spinner("Buscando títulos disponíveis..."):
        anos_disponiveis = obter_anos_disponiveis()
    
    if not anos_disponiveis:
        st.error("❌ Não foi possível carregar os títulos. Verifique sua conexão.")
        return
    # Input da taxa
    taxa_anual = st.sidebar.number_input(
        "📈 Taxa anual (%):",
        min_value=0.01,
        max_value=50.0,
        value=13.92,
        step=0.01,
        format="%.2f"
    )
    
    # Botão de cálculo
    calcular = st.sidebar.button("🚀 Calcular", type="primary")
    
    # Layout principal
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 Informações do Título")
        
        if calcular:
            with st.spinner("Calculando..."):
                resultado = calculadora_prefixado_streamlit(ano_selecionado, taxa_anual)
            
            if resultado is None:
                st.error(f"❌ Título para {ano_selecionado} não encontrado!")
            else:
                dados = resultado['dados']
                
                # Informações do título
                st.info(f"**Título:** {dados['nome']}")
                st.info(f"**Vencimento:** {dados['vencimento']}")
                st.info(f"**Valor Nominal:** R$ {dados['valor_nominal']:,.2f}")
                st.info(f"**Data da Consulta:** {dados['data_consulta']}")
                
                # Informações de prazo
                st.subheader("📅 Informações de Prazo")
                st.success(f"**Dias Corridos:** {resultado['dias_corridos']}")
                st.success(f"**Dias Úteis:** {resultado['dias_uteis']}")
    
    with col2:
        st.subheader("🔢 Resultado do Cálculo")
        
        if calcular and resultado is not None:
            # Destaque do resultado principal
            st.metric(
                label="💎 Preço Unitário (PU)",
                value=f"R$ {resultado['pu_calculado']:,.6f}",
                delta=None
            )
            
            st.metric(
                label="📊 Taxa Utilizada",
                value=f"{resultado['taxa_usada']:.2f}% a.a.",
                delta=None
            )
            
           
    
    # Seção de informações adicionais
    st.markdown("---")
    st.subheader("📚 Informações Importantes")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🎯 O que é o Tesouro Prefixado?**
        
        Título público com rentabilidade definida no momento da compra. 
        Você sabe exatamente quanto receberá no vencimento.
        """)
    
    with col2:
        st.warning("""
        **⚠️ Atenção**
        
        Os valores são calculados com base na fórmula oficial. 
        Confirme sempre no site oficial do Tesouro Direto.
        """)
    
    with col3:
        st.success("""
        **📖 Fórmula Utilizada**
        
        PU = VN / [(Taxa/100 + 1)^(du/252)]
        
        Onde:
        - VN = Valor Nominal (R$ 1.000)
        - du = Dias Úteis
        """)

if __name__ == "__main__":
    main()