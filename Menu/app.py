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
            # 1. Logo Adaptável
            import base64
            
            def get_b64(path):
                try:
                    with open(path, "rb") as f:
                        return base64.b64encode(f.read()).decode()
                except:
                    return ""

            try:
                img_dir = os.path.join(os.path.dirname(__file__), "images")
                path_dark = os.path.join(img_dir, "Logo_BRG.png")
                path_light = os.path.join(img_dir, "Logo_BRGTemaClaro.png")
                
                b64_d = get_b64(path_dark)
                b64_l = get_b64(path_light)
                
                if not b64_l: b64_l = b64_d

                # CSS Lateral (Inline para garantir escopo)
                st.markdown("""
                <style>
                    /* Sidebar Logo Toggle */
                    .sidebar-logo-dark { display: block !important; margin-bottom: 20px; width: 100%; }
                    .sidebar-logo-light { display: none !important; margin-bottom: 20px; width: 100%; }

                    [data-theme="light"] .sidebar-logo-dark,
                    section[data-theme="light"] .sidebar-logo-dark,
                    div[data-theme="light"] .sidebar-logo-dark {
                         display: none !important; 
                    }
                    
                    [data-theme="light"] .sidebar-logo-light,
                    section[data-theme="light"] .sidebar-logo-light,
                    div[data-theme="light"] .sidebar-logo-light {
                         display: block !important; 
                    }
                    
                    @media (prefers-color-scheme: light) {
                         .sidebar-logo-dark { display: none !important; }
                         .sidebar-logo-light { display: block !important; }
                    }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown(
                    f"""
                    <div>
                        <img src='data:image/png;base64,{b64_d}' class='sidebar-logo-dark'>
                        <img src='data:image/png;base64,{b64_l}' class='sidebar-logo-light'>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            except Exception:
                # Fallback
                st.image(path_dark, use_container_width=True)

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