import pandas as pd
import os
from datetime import datetime
import streamlit as st

LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "access_logs.csv")

def log_access(report_name, user_email, user_name):
    """
    Registra o acesso de um usuário a um relatório.
    
    Args:
        report_name (str): Nome do relatório acessado.
        user_email (str): E-mail do usuário.
        user_name (str): Nome do usuário.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = {
        "Data/Hora": timestamp,
        "Relatório": report_name,
        "Usuário (Email)": user_email,
        "Usuário (Nome)": user_name
    }
    
    try:
        if not os.path.exists(LOG_FILE_PATH):
            df = pd.DataFrame([new_entry])
            df.to_csv(LOG_FILE_PATH, index=False)
        else:
            # Append sem carregar tudo se possível, mas pandas precisa ler header
            # Vamos usar modo 'a' do pandas
            df = pd.DataFrame([new_entry])
            df.to_csv(LOG_FILE_PATH, mode='a', header=False, index=False)
            
    except Exception as e:
        print(f"Erro ao salvar log: {e}")
        # Silencioso para o usuário final, mas idealmente logado no servidor

def get_logs():
    """
    Retorna todos os logs de acesso.
    
    Returns:
        pd.DataFrame: DataFrame com os logs.
    """
    if not os.path.exists(LOG_FILE_PATH):
        return pd.DataFrame(columns=["Data/Hora", "Relatório", "Usuário (Email)", "Usuário (Nome)"])
    
    try:
        return pd.read_csv(LOG_FILE_PATH)
    except Exception as e:
        st.error(f"Erro ao ler logs: {e}")
        return pd.DataFrame()
