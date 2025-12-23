import streamlit as st
from backend.db import build_connection_string, connect

# Admin Hardcoded (Único que tem acesso à engrenagem)
ADMIN_EMAIL = "eduardo.marconi@brggeradores.com.br"

def _ensure_table_exists():
    """Garante que a tabela de permissões existe no banco."""
    conn_str = build_connection_string()
    try:
        with connect(conn_str) as conn:
            cursor = conn.cursor()
            # Tenta criar a tabela se não existir
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='AppPermissions' AND xtype='U')
                CREATE TABLE AppPermissions (
                    report_key VARCHAR(50),
                    user_email VARCHAR(200)
                )
            """)
            conn.commit()
    except Exception as e:
        st.error(f"Erro ao inicializar tabela de permissões: {e}")

def load_permissions():
    """Carrega as permissões do Banco de Dados. Retorna um dict."""
    _ensure_table_exists()
    
    permissions = {}
    conn_str = build_connection_string()
    
    try:
        with connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT report_key, user_email FROM AppPermissions")
            rows = cursor.fetchall()
            
            for row in rows:
                key = row.report_key
                email = row.user_email
                if key not in permissions:
                    permissions[key] = []
                permissions[key].append(email)
                
        # Garante que Admin sempre está na lista (memória)
        if "stock" not in permissions:
             permissions["stock"] = []
        if ADMIN_EMAIL not in permissions["stock"]:
             permissions["stock"].append(ADMIN_EMAIL)
             
        return permissions

    except Exception as e:
        st.error(f"Erro ao carregar permissões do banco: {e}")
        return {"stock": [ADMIN_EMAIL]}

def save_permissions(data):
    """Salva as permissões no Banco de Dados (Limpa e reescreve)."""
    conn_str = build_connection_string()
    try:
        with connect(conn_str) as conn:
            cursor = conn.cursor()
            
            # 1. Limpa tabela
            cursor.execute("DELETE FROM AppPermissions")
            
            # 2. Insere novos dados
            for key, emails in data.items():
                for email in emails:
                    # Normaliza
                    safe_email = email.strip().lower()
                    if safe_email:
                        cursor.execute("INSERT INTO AppPermissions (report_key, user_email) VALUES (?, ?)", (key, safe_email))
            
            conn.commit()
            
    except Exception as e:
        st.error(f"Erro ao salvar permissões no banco: {e}")

def check_user_access(user_email, report_key):
    """
    Verifica se o usuário tem acesso ao relatório.
    """
    if user_email.lower() == ADMIN_EMAIL.lower():
        # Admin sempre pode
        return True
    
    perms = load_permissions()
    allowed_list = perms.get(report_key, [])
    
    # Normaliza para lower case para evitar problemas
    allowed_list = [email.lower() for email in allowed_list]
    
    return user_email.lower() in allowed_list

    #Teste de permissão
