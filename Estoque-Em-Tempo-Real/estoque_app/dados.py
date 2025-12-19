import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path

from backend.db import build_connection_string, connect

BASE_DIR = Path(__file__).resolve().parents[1]
# Tenta novo caminho (backend/queries). Mantem fallback para caminho antigo (queries/) se precisar.
ESTOQUE_SQL_PATHS = [
    BASE_DIR / "backend" / "queries" / "estoque.sql",
    BASE_DIR / "queries" / "estoque.sql",
]


# Tenta carregar a query SQL de dois locais possíveis
# Isso ajuda a evitar erros se a estrutura de pastas mudar
def load_query():
    """Lê o arquivo .sql que contém o comando para buscar os dados."""
    for path in ESTOQUE_SQL_PATHS:
        if path.exists():
            return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Não encontrei o arquivo estoque.sql em: {[str(p) for p in ESTOQUE_SQL_PATHS]}")


@st.cache_data(ttl=300, show_spinner="Consultando o estoque no banco de dados...")
def buscar_dados_estoque():
    """
    Conecta ao SQL Server, executa a consulta e retorna os dados em uma tabela (DataFrame).
    
    O decorador @st.cache_data faz com que o resultado fique salvo na memória por 5 minutos (300s),
    para não precisarmos ir ao banco de dados toda hora (dá mais performance).
    """
    # 1. Tenta criar a 'string de conexão' (o endereço e senha do banco)
    try:
        # Pela implementação do backend.db, se não passar argumentos,
        # ele tenta ler de backend/secrets.toml automaticamente
        connection_string = build_connection_string()
    except (KeyError, FileNotFoundError) as e:
        st.error(f"Erro de configuração: Não consegui ler as senhas. Detalhe: {e}")
        return pd.DataFrame()

    # 2. Conecta e busca os dados
    try:
        with connect(connection_string) as conn:
            # pd.read_sql roda o comando SQL e já devolve uma tabela bonita do Pandas
            df = pd.read_sql(load_query(), conn)
    except FileNotFoundError as e:
        st.error(f"Erro de arquivo: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar dados: Verifique a conexão com a internet ou VPN. Detalhe: {e}")
        return pd.DataFrame()

    # 3. Limpeza e arrumação dos dados
    
    # Se existir a coluna de data da última saída, vamos arrumar o formato dela
    if "DtUltimaSaida" in df.columns:
        # Pega a coluna e garante que é texto (str), tirando espaços em branco extras
        dt_col = df["DtUltimaSaida"].astype(str).str.strip()
        
        # Substitui valores vazios ou zerados por "Nada" (pd.NA), pois não são datas válidas
        dt_col = dt_col.replace({"": pd.NA, " ": pd.NA, "0": pd.NA, "00000000": pd.NA})

        # Procura por datas no formato YYYYMMDD (8 dígitos seguidos)
        mask_8digits = dt_col.str.fullmatch(r"\d{8}", na=False)
        if mask_8digits.any():
            # Converte esses 8 dígitos para data real
            dt_col.loc[mask_8digits] = pd.to_datetime(dt_col[mask_8digits], format="%Y%m%d", errors="coerce")

        # Converte o resto (o que o Pandas conseguir entender automaticamente)
        dt_col = pd.to_datetime(dt_col, errors="coerce")
        
        # Guarda apenas a parte da DATA (ignora hora) na coluna original
        df["DtUltimaSaida"] = dt_col.dt.date

    # Garante que colunas numéricas essenciais sejam números de fato (e não texto),
    # preenchendo vazios com 0. Isso roda aqui para aproveitar o cache (não roda em todo render).
    colunas_numericas = ["SaldoEmEstoque", "EmpenhoReqPvReserva", "EstoqueDisponivel"]
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Marca o horário que buscamos esses dados (para mostrar no rodapé depois)
    df.attrs["fetched_at"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    return df

