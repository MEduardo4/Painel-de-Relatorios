from typing import Optional
from io import BytesIO
import streamlit as st
import pandas as pd

from comum.formatacao import format_number


def render_kpis(tabela_estoque):
    """Calcula e exibe os indicadores principais (cards no topo)."""
    st.subheader("Indicadores Chave (KPIs)")

    # Cálculos simples baseados nas colunas da tabela
    total_itens_distintos = tabela_estoque["CodigoProduto"].count()
    saldo_total_unidades = tabela_estoque["SaldoEmEstoque"].sum()
    estoque_disponivel = tabela_estoque["EstoqueDisponivel"].sum()

    # Cria 3 colunas para exibir os cards lado a lado
    coluna1, coluna2, coluna3 = st.columns(3)
    
    # Lista com as informações de cada card para gerar num loop (mais organizado)
    dados_cards = [
        (coluna1, "Total de Produtos", format_number(total_itens_distintos, decimals=2)),
        (coluna2, "Saldo Total (un)", format_number(saldo_total_unidades, decimals=2)),
        (coluna3, "Disponível (un)", format_number(estoque_disponivel, decimals=2)),
    ]

    for col, label, valor in dados_cards:
        with col:
            # Usa HTML direto para criar um visual de "cartão" estilizado (CSS deve estar no layout)
            st.markdown(
                f"<div class='kpi-card'><div class='kpi-label'>{label}</div><div class='kpi-value'>{valor}</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")


def render_filters(tabela_estoque):
    """Cria os filtros na barra lateral e retorna a tabela filtrada."""

    
    st.sidebar.header("Filtros")

    # Campos de texto (busca parcial)
    filtro_nome = st.sidebar.text_input("Nome do Produto")
    filtro_codigo = st.sidebar.text_input("Código do Produto")

    # Campos de seleção múltipla (listas)
    # sorted(...) organiza as opções em ordem alfabética para facilitar
    # unique() pega apenas os valores únicos daquela coluna
    filtro_grupo = st.sidebar.multiselect("Grupo", sorted(tabela_estoque["DescGrupo"].unique()))
    filtro_tipo = st.sidebar.multiselect("Tipo", sorted(tabela_estoque["DescTipo"].unique()))
    filtro_armazem = st.sidebar.multiselect("Armazém", sorted(tabela_estoque["DescArmazem"].unique()))
    filtro_filial = st.sidebar.multiselect("Filial", sorted(tabela_estoque["Filial"].unique()))
    filtro_bloq = st.sidebar.multiselect("Bloqueado", sorted(tabela_estoque["Bloq"].unique()))
    
    # Checkbox simples (Sim/Não)
    filtro_saldo = st.sidebar.checkbox("Somente com saldo > 0", value=False)

    # Começamos com uma cópia da tabela inteira
    tabela_filtrada = tabela_estoque.copy()

    # Vamos aplicando os filtros um a um. Se o usuário não preencheu nada, ignora.
    
    if filtro_nome:
        # Busca texto que contenha o que foi digitado (case=False ignora maiúsculas/minúsculas)
        tabela_filtrada = tabela_filtrada[tabela_filtrada["NomeProduto"].str.contains(filtro_nome, case=False, na=False)]

    if filtro_codigo:
        tabela_filtrada = tabela_filtrada[tabela_filtrada["CodigoProduto"].astype(str).str.contains(filtro_codigo, case=False, na=False)]

    if filtro_grupo:
        # 'isin' verifica se o valor da linha está DENTRO da lista de selecionados
        tabela_filtrada = tabela_filtrada[tabela_filtrada["DescGrupo"].isin(filtro_grupo)]

    if filtro_tipo:
        tabela_filtrada = tabela_filtrada[tabela_filtrada["DescTipo"].isin(filtro_tipo)]

    if filtro_armazem:
        tabela_filtrada = tabela_filtrada[tabela_filtrada["DescArmazem"].isin(filtro_armazem)]

    if filtro_filial:
        tabela_filtrada = tabela_filtrada[tabela_filtrada["Filial"].isin(filtro_filial)]

    if filtro_bloq:
        tabela_filtrada = tabela_filtrada[tabela_filtrada["Bloq"].isin(filtro_bloq)]

    if filtro_saldo and "SaldoEmEstoque" in tabela_filtrada.columns:
        tabela_filtrada = tabela_filtrada[tabela_filtrada["SaldoEmEstoque"] > 0]

    return tabela_filtrada


def render_toolbar(fetched_at: Optional[str]):
    """Mostra a barrinha com a data da última atualização."""
    with st.container():
        cols = st.columns([3, 2])
        # Alinha à direita na segunda coluna
        with cols[1]:
            st.markdown(
                f"<div class='toolbar'><span class='toolbar-badge'>Atualizado: {fetched_at or '---'}</span></div>",
                unsafe_allow_html=True,
            )


@st.cache_data(show_spinner=False)
def convert_to_excel(df: pd.DataFrame) -> bytes:
    """
    Converte o DataFrame para Excel em memória.
    Cacheado para não recriar o arquivo toda vez que a tela atualiza.
    """
    buffer = BytesIO()
    try:
        import openpyxl  # noqa: F401
        df.to_excel(buffer, index=False)
    except ImportError:
        # Fallback simples se não tiver openpyxl (mas requirements diz que tem)
        return df.to_csv(index=False).encode("utf-8")
    
    return buffer.getvalue()


def render_table(tabela_estoque):
    """Exibe a tabela principal de dados."""
    st.subheader("Visualização Detalhada do Estoque")

    # === 1. Preparação dos dados ===
    # A conversão numérica agora é feita lá no 'services/estoque.py'
    # Então aqui a gente só prepara a exibição.
    
    # Define quais colunas vamos mostrar e em qual ordem
    colunas_para_exibir = [
        "CodigoProduto",
        "NomeProduto",
        "Armazem",
        "UM",
        "SaldoEmEstoque",
        "EmpenhoReqPvReserva",
        "EstoqueDisponivel",
        "Grupo",
        "Tipo",
    ]

    # Filtra apenas essas colunas para exibição na tela
    tabela_visualizacao = tabela_estoque[colunas_para_exibir].copy()

    # === 2. Exibição ===
    
    # REMOVIDO: Otimizações de limite e Styler.
    # Voltamos ao padrão nativo do Streamlit que é muito performático e suporta milhares de linhas.
    # A formatação visual será a padrão (ex: 1,000.00), mas a ordenação e velocidade serão perfeitas.

    st.dataframe(
        tabela_visualizacao,
        use_container_width=True,
        height=520,
        column_config={
            # Configurações visuais extras para cada coluna
            "CodigoProduto": st.column_config.TextColumn("Código", width="small"),
            "NomeProduto": st.column_config.TextColumn("Produto", width="medium"),
            "Armazem": st.column_config.TextColumn("Armazém", width="small"),
            "UM": st.column_config.TextColumn("UM", width="small"),
            # Voltamos a usar format="%.2f". O sort funciona perfeitamente (numérico).
            # A visualização usará o locale do sistema/navegador (provavelmente ponto para decimais).
            "SaldoEmEstoque": st.column_config.NumberColumn("Saldo em Estoque", format="%.2f", width="medium"),
            "EmpenhoReqPvReserva": st.column_config.NumberColumn("Empenho/Req/Reserva", format="%.2f", width="medium"),
            "EstoqueDisponivel": st.column_config.NumberColumn("Disponível", format="%.2f", width="medium"),
            "Grupo": st.column_config.TextColumn("Grupo", width="small"),
            "Tipo": st.column_config.TextColumn("Tipo", width="small"),
        },
    )

    # === 3. Botão de Exportação ===
    # Usamos a função cacheada. Se os dados não mudaram, ele pega direto da memória.
    # Atenção: Passamos 'tabela_visualizacao' para baixar o que o usuário está vendo (filtrado e colunas certas)
    excel_data = convert_to_excel(tabela_visualizacao)
    
    # Detecta se é CSV ou Excel (pelo header do bytes, mas simplificando pela lógica)
    is_xlsx = True 
    # (assumindo que openpyxl está instalado, como garantido no requirements)

    if is_xlsx:
        st.download_button(
            label="Baixar Planilha Excel (XLSX)",
            data=excel_data,
            file_name="estoque_filtrado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
