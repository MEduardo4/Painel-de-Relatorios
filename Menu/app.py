import streamlit as st
from datetime import datetime

from comum.layout import setup_page


def main():
    # 0. Configura página primeiro
    setup_page()

    # 1. Ajusta PATH para importar projetos vizinhos
    import sys
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__)) # .../Relatorios/Menu
    relatorios_dir = os.path.dirname(current_dir) # .../Relatorios
    
    if relatorios_dir not in sys.path:
        sys.path.append(relatorios_dir)
    
    # Caminho do Projeto de Estoque
    estoque_project_path = os.path.join(relatorios_dir, "Estoque-Em-Tempo-Real")
    
    if estoque_project_path not in sys.path:
        sys.path.append(estoque_project_path)

    # 2. Verifica Autenticação
    from Menu.login import check_authentication, render_login
    from Menu.admin_panel import render_admin_panel # Importa aqui para evitar erro de escopo
    
    if not check_authentication():
        render_login()
        return

    # Se chegou aqui, está logado!
    # Roteamento
    # Define a página atual (padrão="menu")
    current_page = st.session_state.get("current_page", "menu")

    # Mover sidebar para cá e condicionar
    if current_page not in ["menu", "admin"]:
        user_info = st.session_state.get("user_info", {})
        user_name = user_info.get("name", "Usuário")
        
        # Sidebar Global (Aparece apenas se NÃO for menu)
        with st.sidebar:
            # 1. Logo
            logo_path = os.path.join(os.path.dirname(__file__), "images", "Logo_BRG.png")
            st.image(logo_path, use_container_width=True)

            # 2. Navegação
            if current_page != "admin":
                if st.button("⬅️ Voltar ao Menu", use_container_width=True):
                    st.session_state["current_page"] = "menu"
                    st.rerun()
            
            # Espaço para os filtros entrarem aqui...

    if current_page == "menu":
        from Menu.home import render_home_menu
        render_home_menu()

    elif current_page == "stock":
        # Relatório de Estoque
        from estoque_app.pagina import render_stock_report
        render_stock_report()

    elif current_page == "admin":
        # Painel Administrativo
        render_admin_panel()

    # Rodapé da Sidebar (Aparece após os filtros do relatório)
    if current_page not in ["menu", "admin"]:
        user_info = st.session_state.get("user_info", {})
        user_name = user_info.get("name", "Usuário")
        
        with st.sidebar:
            st.markdown("---")
            # 3. User Info (Agora no final)
            st.success(f"Logado como:\n**{user_name}**")
            if st.button("Sair", use_container_width=True):
                st.session_state.clear()
                st.rerun()


# Bloco padrão do Python: Garante que o main só rode se executarmos esse arquivo diretamente
if __name__ == "__main__":
    main()



# criar log de acesso 