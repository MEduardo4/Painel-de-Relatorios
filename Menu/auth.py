import msal
import os
import streamlit as st # Necessário para acessar secrets

# --- CONFIGURAÇÃO DE CREDENCIAIS (Via Secrets do Streamlit) ---
# As chaves ficam em .streamlit/secrets.toml
CLIENT_ID = st.secrets["azure"]["client_id"]
TENANT_ID = st.secrets["azure"]["tenant_id"]
CLIENT_SECRET = st.secrets["azure"]["client_secret"]
# -----------------------------------------------------------

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/"  # A aplicação roda na raiz
# Se rodar localmente, o Streamlit costuma usar http://localhost:8501 ou 8507
# Confirme a porta que o seu app está usando e registre no Azure URI de Redirecionamento
# Ex: http://localhost:8507/
#
def get_redirect_uri():
    """Helper para obter a URI de redirecionamento correta."""
    if "azure" in st.secrets and "redirect_uri" in st.secrets["azure"]:
        return st.secrets["azure"]["redirect_uri"]
    
    # Detecção básica de ambiente
    if os.getenv("STREAMLIT_SERVER_PORT"):
        return f"http://localhost:{os.getenv('STREAMLIT_SERVER_PORT')}/"
        
    return "https://painel-de-relatorios.streamlit.app/"

SCOPE = ["User.Read"]

class AuthService:
    def __init__(self):
        self.app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET,
        )

    def get_auth_url(self, redirect_uri):
        """Gera a URL de login da Microsoft."""
        auth_url = self.app.get_authorization_request_url(
            SCOPE,
            redirect_uri=redirect_uri
        )
        return auth_url

    def get_token_from_code(self, code, redirect_uri):
        """Troca o código de autorização pelo token de acesso."""
        result = self.app.acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,
            redirect_uri=redirect_uri
        )
        return result

    def get_user_info(self, token):
        """(Opcional) Usa o token para pegar mais dados via Microsoft Graph."""
        import requests
        graph_data = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={'Authorization': 'Bearer ' + token}
        ).json()
        return graph_data
