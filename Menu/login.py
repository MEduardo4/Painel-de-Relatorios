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
            .login-button {
                display: block;
                width: 100%;
                background-color: #EF4444;
                color: #FFFFFF !important;
                text-decoration: none;
                text-align: center;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 10px;
                transition: background-color 0.3s;
            }
            .login-button:hover {
                background-color: #DC2626;
                text-decoration: none;
            }
            .login-button:visited {
                color: #FFFFFF !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # ... (código intermediário omitido, mantendo o fluxo)
    # Se certifique de manter o fluxo

    # Layout Centralizado
    col_left, col_center, col_right = st.columns([1, 1.2, 1])

    with col_center:
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
            <a href="{auth_url}" target="_top" class="login-button">
                🔐 Entrar com Microsoft
            </a>
            <div style="text-align: center; margin-top: 10px;">
                <a href="{auth_url}" target="_top" style="color: #94A3B8; font-size: 12px;">(Link direto alternativo)</a>
            </div>
        """, unsafe_allow_html=True)
        
        # DEBUG DE SOBREVIVÊNCIA: Se o botão falhar, o link cru funciona
        st.write("---")
        st.warning("Se o botão acima não funcionar, clique no link abaixo:")
        st.write(f"Link Bruto: {auth_url}")
        st.write("---")

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

    # Tenta pegar 'code' de qualquer formato (dict ou list)
    code = None
    if "code" in query_params:
        val = query_params["code"]
        if isinstance(val, list):
             code = val[0]
        else:
             code = val

    if code:
        try:
            from Menu.auth import AuthService, get_redirect_uri
        except ImportError:
             from .auth import AuthService, get_redirect_uri
             
        auth_service = AuthService()
        redirect_uri = get_redirect_uri()
        
        try:
            token_result = auth_service.get_token_from_code(code, redirect_uri)
            if "access_token" in token_result:
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = token_result.get("id_token_claims", {})
                st.session_state["access_token"] = token_result["access_token"]
                
                # Limpa o código da URL para ficar limpo
                st.query_params.clear()
                st.rerun()
                return True
            else:
                st.error(f"Erro de Autenticação: {token_result.get('error_description')}")
        except Exception as e:
            st.error(f"Ocorreu um erro durante o login: {str(e)}")
            
    # Se chegou aqui é porque não autenticou
    if "code" in query_params and not st.session_state.get("authenticated", False):
         st.warning("⚠️ O sistema detectou um retorno do login, mas a sessão não foi persistida. Isso pode indicar bloqueio de Cookies ou problema de configuração no Streamlit Cloud.")
         
    return False
