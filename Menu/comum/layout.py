import streamlit as st


def setup_page():
    st.set_page_config(page_title="Estoque em Tempo Real", layout="wide")


def render_header():
    st.markdown(
        """
        <div style="
            background-color: var(--secondary-background-color);
            padding: 18px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid var(--background-color);
            margin-bottom: 20px;
        ">
            <h2 style='color: var(--text-color); margin: 0; padding: 0; letter-spacing: 0.5px;'>
                Estoque em Tempo Real
            </h2>
            <p style='color: var(--text-color); margin: 4px 0 0 0; font-size: 14px; opacity: 0.7;'>
                Monitoramento em tempo real com filtros rapidos e KPIs
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def inject_styles():
    st.markdown(
        <style>
            :root {
                /* Usar variáveis do Streamlit para adaptação */
                --card-bg: var(--secondary-background-color);
                --card-border: var(--background-color);
            }
            
            /* Melhoria visual nos inputs da Sidebar (sem forçar cor preta) */
            section[data-testid="stSidebar"] .stTextInput > div > div,
            section[data-testid="stSidebar"] .stSelectbox > div > div,
            section[data-testid="stSidebar"] .stMultiSelect > div > div {
                border-radius: 10px !important;
            }
            
            .yellow-header {
                background-color: #FACC15;
                color: #0F172A;
                padding: 5px;
                border-radius: 5px 5px 0 0;
                text-align: center;
                font-weight: bold;
                margin-bottom: -5px;
                border: 1px solid var(--background-color);
                border-bottom: none;
            }
            
            .kpi-card {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 12px;
                padding: 12px 14px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            
            .kpi-label {
                color: var(--text-color);
                font-size: 12px;
                margin-bottom: 4px;
                letter-spacing: 0.3px;
                opacity: 0.8;
            }
            
            .kpi-value {
                color: var(--primary-color);
                font-size: 22px;
                font-weight: 700;
            }
            
            .kpi-sub {
                color: var(--text-color);
                font-size: 12px;
                opacity: 0.6;
            }
            
            .toolbar {
                display: flex;
                gap: 8px;
                align-items: center;
                justify-content: flex-end;
                margin-bottom: 10px;
            }
            
            .toolbar-badge {
                background: var(--secondary-background-color);
                color: var(--text-color);
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 12px;
                border: 1px solid var(--background-color);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
