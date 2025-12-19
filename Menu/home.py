import streamlit as st

def render_home_menu():
    """Renderiza o Menu Principal com opções de relatórios."""
    
from Menu.permissions import ADMIN_EMAIL

def render_home_menu():
    """Renderiza o Menu Principal com opções de relatórios."""
    
    # Pega info do usuário para dar Oi
    user_info = st.session_state.get("user_info", {})
    user_name = user_info.get("name", "Usuário")
    user_email = user_info.get("preferred_username", "").lower()

    # Header com Título, Botão Admin (se for o caso) e Botão de Sair
    # Layout [Texto largo | Botão Admin (se houver) | Botão Sair]
    
    is_admin = user_email == ADMIN_EMAIL.lower()
    
    if is_admin:
        col_header, col_admin, col_sair = st.columns([11, 1, 1], vertical_alignment="bottom")
    else:
        col_header, col_sair = st.columns([12, 1], vertical_alignment="bottom")

    with col_header:
        st.title("Painel de Relatórios")
        st.subheader(f"Bem-vindo, {user_name}!")
    
    # Renderiza botão admin se aplicável
    if is_admin:
        with col_admin:
            if st.button("⚙️", help="Gerenciar Acessos", use_container_width=True):
                st.session_state["current_page"] = "admin"
                st.rerun()

    with col_sair:
        if st.button("Sair", type="secondary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("---")

    st.caption("Selecione o relatório que deseja acessar:")

    # Layout de "Cards" usando colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        # Card 1: Estoque
        with st.container(border=True):
            st.markdown("### 📦 Estoque em Tempo Real")
            st.markdown("Visão geral em tempo real, status de ocupação e produtos.")
            if st.button("Acessar Relatório", key="btn_estoque", type="primary", use_container_width=True):
                st.session_state['current_page'] = "stock"
                st.rerun()

    # Futuros relatórios podem entrar em col2, col3...
    with col2:
        # Exemplo de placeholder para futuro
        with st.container(border=True):
            st.markdown("### 📊 Vendas (Futuro)")
            st.markdown("Relatórios de faturamento e performance comercial.")
            st.button("Em breve", disabled=True, use_container_width=True)
