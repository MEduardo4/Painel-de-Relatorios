import streamlit as st
import os
try:
    from Menu.auth import AuthService, get_redirect_uri
except ImportError:
    from .auth import AuthService, get_redirect_uri
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def render_login():
    """Renderiza a página de login com visual aprimorado."""
    
    # CSS Customizado
    st.markdown("""
        <style>
            .login-subtext {
                font-size: 14px;
                color: #94A3B8;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Layout Centralizado
    col_left, col_center, col_right = st.columns([1, 1.2, 1])

    with col_center:
        st.error("⚠️ VERSÃO DEBUG: 99.1 - CHECANDO DEPLOY ⚠️")
        st.write(f"URI esperada: {get_redirect_uri()}")
        
        # Espaçamento vertical
        st.write("")
        st.write("")
        
        # Logo Centralizado via HTML (Infalível)
        try:
            img_path = os.path.join(os.path.dirname(__file__), "images", "Logo_BRG.png")
            img_b64 = get_base64_image(img_path)
            st.markdown(
                f"<div style='display: flex; justify-content: center; margin-bottom: 20px;'>"
                f"<img src='data:image/png;base64,{img_b64}' width='500'>"
                f"</div>",
                unsafe_allow_html=True
            )
        except Exception:
            # Fallback caso não ache a imagem
            img_path = os.path.join(os.path.dirname(__file__), "images", "Logo_BRG.png")
            st.image(img_path, width=600)

        st.markdown("<h3 style='text-align: center; color: #F8FAFC;'>Painel de Relatórios</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;' class='login-subtext'>Entre com sua conta corporativa para acessar</p>", unsafe_allow_html=True)

        # Lógica de Autenticação
        auth_service = AuthService()
        redirect_uri = get_redirect_uri()
        
        # Gera URL direto e mostra botão único
        auth_url = auth_service.get_auth_url(redirect_uri)
        
        st.markdown(f"""
            <a href="{auth_url}" target="_self" style="text-decoration: none;">
                <button style="
                    width: 100%;
                    background-color: #EF4444;
                    color: #FFFFFF;
                    border: none;
                    padding: 12px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 10px;
                    transition: background-color 0.3s;
                " onmouseover="this.style.backgroundColor='#DC2626'" onmouseout="this.style.backgroundColor='#EF4444'">
                    🔐 Entrar com Microsoft
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("")

def check_authentication():
    """
    Verifica se o usuário está logado ou se acabou de voltar do login.
    Retorna True se logado, False caso contrário.
    """
    
    # 1. Se já está na sessão, OK
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        return True

    # 2. Se voltou do Azure com um código na URL
    query_params = st.query_params
    if "code" in query_params:
        st.info(f"DEBUG: CÓDIGO RECEBIDO DE AZURE! {query_params['code']}")
        st.warning("Se você está lendo isso, o loop parou AQUI.")
        st.stop()
        
    return False
