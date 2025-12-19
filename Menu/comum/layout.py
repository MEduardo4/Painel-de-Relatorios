import streamlit as st


def setup_page():
    st.set_page_config(page_title="Estoque em Tempo Real", layout="wide")


def render_header():
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
            padding: 18px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        ">
            <h2 style='color: #F8FAFC; margin: 0; padding: 0; letter-spacing: 0.5px;'>
                Estoque em Tempo Real
            </h2>
            <p style='color: #CBD5E1; margin: 4px 0 0 0; font-size: 14px;'>
                Monitoramento em tempo real com filtros rapidos e KPIs
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def inject_styles():
    st.markdown(
        """
        <style>
            :root {
                --card-bg: #0F172A;
                --card-border: #1E293B;
                --accent: #38BDF8;
                --accent-2: #FACC15;
            }
            /* Sidebar: inputs e selects com estilo uniforme */
            section[data-testid="stSidebar"] .stTextInput > div > div input,
            section[data-testid="stSidebar"] .stTextInput > div > div textarea,
            section[data-testid="stSidebar"] .stSelectbox > div > div,
            section[data-testid="stSidebar"] .stMultiSelect > div > div {
                background: #111827 !important;
                color: #E2E8F0 !important;
                border: 1px solid #475569 !important;
                border-radius: 10px !important;
                padding: 10px 12px !important;
            }
            section[data-testid="stSidebar"] .stTextInput > label,
            section[data-testid="stSidebar"] .stSelectbox > label,
            section[data-testid="stSidebar"] .stMultiSelect > label {
                color: #e2e8f0 !important;
                font-weight: 600;
            }
            section[data-testid="stSidebar"] .stTextInput input::placeholder {
                color: #94A3B8 !important;
            }
            .yellow-header {
                background-color: #FACC15;
                color: #0F172A;
                padding: 5px;
                border-radius: 5px 5px 0 0;
                text-align: center;
                font-weight: bold;
                margin-bottom: -5px;
                border: 1px solid #E2E8F0;
                border-bottom: none;
            }
            .kpi-card {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 12px;
                padding: 12px 14px;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
            }
            .kpi-label {
                color: #E2E8F0;
                font-size: 12px;
                margin-bottom: 4px;
                letter-spacing: 0.3px;
            }
            .kpi-value {
                color: #F8FAFC;
                font-size: 22px;
                font-weight: 700;
            }
            .kpi-sub {
                color: #94A3B8;
                font-size: 12px;
            }
            .toolbar {
                display: flex;
                gap: 8px;
                align-items: center;
                justify-content: flex-end;
                margin-bottom: 10px;
            }
            .toolbar-badge {
                background: #E2E8F0;
                color: #0F172A;
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 12px;
                border: 1px solid #CBD5E1;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
