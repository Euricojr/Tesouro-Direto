# 🇧🇷 Tesouro Direto Apreçamento 

## 🚧 Status do Projeto
Em desenvolvimento/manutenção.

## ✨ Sobre o Projeto

Este projeto em Python tem como foco a **precificação de títulos públicos federais** negociados no Tesouro Direto, seguindo rigorosamente os critérios e a metodologia de apreçamento estabelecida pela **B3 (Brasil, Bolsa, Balcão)**.

A ferramenta é essencial para investidores e analistas que buscam validar ou calcular o **Valor Justo** (Marcação a Mercado) de diferentes classes de títulos:

* **Prefixados (LTN/NTN-F)**
* **Tesouro IPCA+ (NTN-B)**
* **Tesouro Selic (LFT)**

## 🎯 Objetivo Principal

Implementar os modelos matemáticos e estatísticos utilizados no mercado financeiro brasileiro para calcular as taxas e os preços dos títulos, em conformidade com as diretrizes da B3 e ANBIMA.

## 🔎 Fontes de Dados

Para garantir a precisão na precificação, o projeto utiliza dados de fontes oficiais do mercado financeiro:

| Dado Utilizado | Fonte | URL |
| :--- | :--- | :--- |
| **Taxas e Vencimentos** dos Títulos | Tesouro Direto | `https://www.tesourodireto.com.br/produtos/dados-sobre-titulos/historico-de-precos-e-taxas` |
| **Projeção Mensal do IPCA** (Inflação) | ANBIMA (Projeção de Inflação GP-M) | `https://www.anbima.com.br/pt_br/informar/estatisticas/precos-e-indices/projecao-de-inflacao-gp-m.htm` |

## ⚙️ Instalação e Execução

Siga os passos abaixo para preparar seu ambiente e rodar a aplicação de análise utilizando o Streamlit.

### Pré-requisitos

Você precisará ter o Python instalado (versão 3.x recomendada).

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Euricojr/Tesouro-Direto.git](https://github.com/Euricojr/Tesouro-Direto.git)
    cd Tesouro-Direto
    ```

2.  **Crie e Ative o Ambiente Virtual (Altamente Recomendado):**
    ```bash
    python -m venv venv
    # Linux/macOS
    source venv/bin/activate
    # Windows (CMD ou PowerShell)
    .\venv\Scripts\activate
    ```

3.  **Instale as Dependências:**
    *Certifique-se de que seu arquivo `requirements.txt` esteja na raiz do projeto e contenha o `streamlit`.*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o Modelo de Precificação (Interface Gráfica):**
    O projeto roda como uma aplicação web interativa usando o Streamlit.

    ```bash
    streamlit run app.py
    ```

    Após a execução, a aplicação será aberta automaticamente no seu navegador, geralmente em `http://localhost:8501`.

### 🧪 Testando a Calculadora em HTML 

Estamos desenvolvendo e testando a calculadora também em formato HTML puro. Para visualizar o arquivo localmente em seu navegador de forma eficiente:

1.  Certifique-se de ter o arquivo `calculadora.html` (ou nome similar) no seu repositório.
2.  Instale a extensão **Live Server** (disponível para VS Code ou outros editores).
3.  Clique com o botão direito no arquivo `calculadora.html` e selecione a opção **"Open with Live Server"**.

Isso abrirá a calculadora em um servidor local temporário, permitindo que você a teste em tempo real.

---

## 📁 Estrutura do Código

A organização do repositório reflete a divisão dos títulos analisados:

---
*Desenvolvido por [Euricojr](https://github.com/Euricojr)*
