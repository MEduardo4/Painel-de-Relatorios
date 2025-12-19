import msal
import os


AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/"  # A aplicação roda na raiz
# Se rodar localmente, o Streamlit costuma usar http://localhost:8501 ou 8507
# Confirme a porta que o seu app está usando e registre no Azure URI de Redirecionamento
# Ex: http://localhost:8507/

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
        # Geralmente o próprio ID Token já tem info basicas (claims)
        # Se precisar chamar a API Graph:
        import requests
        graph_data = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={'Authorization': 'Bearer ' + token}
        ).json()
        return graph_data
