import json
import os
import streamlit as st

# Admin Hardcoded (Único que tem acesso à engrenagem)
ADMIN_EMAIL = "eduardo.marconi@brggeradores.com.br"

# Caminho do arquivo JSON no mesmo diretório deste script
PERMISSIONS_FILE = os.path.join(os.path.dirname(__file__), "permissions.json")

def load_permissions():
    """Carrega as permissões do arquivo JSON. Se não existir, cria padrão."""
    if not os.path.exists(PERMISSIONS_FILE):
        default_data = {
            "stock": [ADMIN_EMAIL], # Admin sempre tem acesso inicial
            # "sales": [] ... futuros relatórios
        }
        save_permissions(default_data)
        return default_data
    
    try:
        with open(PERMISSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar permissões: {e}")
        return {}

def save_permissions(data):
    """Salva as permissões no arquivo JSON."""
    try:
        with open(PERMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar permissões: {e}")

def check_user_access(user_email, report_key):
    """
    Verifica se o usuário tem acesso ao relatório.
    Admin tem acesso a TUDO automaticamente? 
    Não necessariamente, mas para editar ele precisa ver.
    """
    if user_email.lower() == ADMIN_EMAIL.lower():
        # Se for admin, verifica se está na lista (para permitir testes)
        # Se quiser que admin tenha acesso total sempre, descomente abaixo:
        # return True
        pass
    
    perms = load_permissions()
    allowed_list = perms.get(report_key, [])
    
    # Normaliza para lower case para evitar problemas
    allowed_list = [email.lower() for email in allowed_list]
    
    return user_email.lower() in allowed_list
