import streamlit as st
from datetime import datetime
from estoque_app.componentes import render_filters, render_kpis, render_table, render_toolbar
from comum.layout import inject_styles, render_header
from estoque_app.dados import buscar_dados_estoque
from Menu.permissions import check_user_access

def render_stock_report():
    """Calcula e renderiza a tela do Relatório de Estoque."""
    
    # 0. Verificação de Segurança
    user_info = st.session_state.get("user_info", {})
    email = user_info.get("preferred_username", "")
    
    if not check_user_access(email, "stock"):
        st.error("🔒 Acesso Negado. Você não tem permissão para visualizar este relatório.")
        st.info("Entre em contato com o administrador (Eduardo Marconi) para solicitar acesso.")
        return

    # 1. Renderiza cabeçalho e aplica estilos CSS (Específicos deste relatório ou gerais)
    render_header()
    inject_styles()

    # 2. Barra de ferramentas (botão de atualizar)
    toolbar = st.container()
    with toolbar:
        coluna_texto, coluna_botao = st.columns([4, 1])
        with coluna_texto:
            st.caption("Use os filtros na barra lateral para refinar a visão.")
        with coluna_botao:
            if st.button("Atualizar dados", use_container_width=True):
                # Limpa o cache para forçar uma nova busca no banco
                buscar_dados_estoque.clear()
                st.rerun()

    # 3. Busca os dados (Executa a query SQL)
    tabela_estoque = buscar_dados_estoque()
    
    # Pega a data da busca
    data_atualizacao = tabela_estoque.attrs.get("fetched_at") if not tabela_estoque.empty else None

    # Mostra a barrinha de atualização
    render_toolbar(data_atualizacao)

    # Se a tabela veio vazia (erro ou sem dados), avisa e para por aqui
    if tabela_estoque.empty:
        st.warning("Não foi possível carregar os dados. Verifique a consulta ou as credenciais.")
        return

    # 4. Aplica os filtros selecionados na sidebar
    tabela_filtrada = render_filters(tabela_estoque)
    
    # 5. Mostra os KPIs (Indicadores) com base nos dados FILTRADOS
    render_kpis(tabela_filtrada)
    
    # Se depois de filtrar não sobrou nada...
    if tabela_filtrada.empty:
        st.info("Nenhum resultado para os filtros selecionados.")
        return

    # 6. Mostra a tabela detalhada
    render_table(tabela_filtrada)

    # Rodapé simples
    st.caption(f"Dados carregados na inicialização: {data_atualizacao or datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
