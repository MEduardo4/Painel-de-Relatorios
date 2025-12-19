import streamlit as st
import pandas as pd
from Menu.permissions import load_permissions, save_permissions, ADMIN_EMAIL

def render_admin_panel():
    """Renderiza a tela de administração de acessos."""
    st.title("⚙️ Gerenciamento de Acessos")
    st.markdown("---")
    
    # Verifica segurança novamente (redundância)
    user_info = st.session_state.get("user_info", {})
    user_email = user_info.get("preferred_username", "").lower()
    
    if user_email != ADMIN_EMAIL.lower():
        st.error("Acesso Negado. Você não tem permissão para ver esta página.")
        if st.button("Voltar"):
            st.session_state["current_page"] = "menu"
            st.rerun()
        return

    # Botão de voltar
    if st.button("⬅️ Voltar ao Menu"):
        st.session_state["current_page"] = "menu"
        st.rerun()

    st.info("Adicione ou remova e-mails autorizados para cada relatório.")

    # 1. Carregar permissões atuais
    perms = load_permissions()
    
    # 2. Selecionar qual relatório editar
    # Se tivermos mais relatórios no futuro, adicionamos aqui
    reports_map = {
        "stock": "📦 Leitura de Estoque",
        # "sales": "📊 Vendas (Futuro)"
    }
    
    selected_report_key = st.selectbox(
        "Selecione o Relatório:",
        options=list(reports_map.keys()),
        format_func=lambda x: reports_map.get(x, x)
    )
    
    # 3. Mostrar lista atual
    current_emails = perms.get(selected_report_key, [])
    
    # Transforma em string para editar no text_area (um por linha)
    emails_text = "\n".join(current_emails)
    
    new_emails_text = st.text_area(
        "E-mails Autorizados (Um por linha)",
        value=emails_text,
        height=200,
        help="Digite os e-mails que podem acessar este relatório."
    )
    
    # 4. Salvar
    if st.button("Salvar Alterações", type="primary"):
        # Converte de volta para lista
        raw_lines = new_emails_text.split("\n")
        # Limpa espaços e vazios
        cleaned_list = [line.strip().lower() for line in raw_lines if line.strip()]
        
        # Remove duplicatas mantendo ordem? Ou set? Set é melhor
        cleaned_list = list(set(cleaned_list))
        cleaned_list.sort()
        
        # Atualiza dicionário
        perms[selected_report_key] = cleaned_list
        
        # Salva
        save_permissions(perms)
        st.success(f"Lista de acessos para '{reports_map[selected_report_key]}' atualizada com sucesso!")
        st.rerun()

    st.markdown("---")
    st.caption("Nota: O e-mail do administrador tem acesso irrestrito, mesmo se não estiver na lista.")
