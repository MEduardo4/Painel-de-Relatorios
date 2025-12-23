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
    # 1. Carrega imagens em Base64 para CSS
    import os
    import base64

    def get_b64(filename):
        try:
            # Caminho relativo: layout.py está em Menu/comum/ -> subir para Menu/images
            # Menu/comum/../../Menu/images (segurança: usar abspath)
            current_dir = os.path.dirname(os.path.abspath(__file__)) # Menu/comum
            menu_dir = os.path.dirname(current_dir) # Menu
            img_path = os.path.join(menu_dir, "images", filename)
            
            with open(img_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception as e:
            # print(f"Erro ao carregar imagem {filename}: {e}")
            return ""

    b64_dark = get_b64("Logo_BRG.png")
    b64_light = get_b64("Logo_BRGTemaClaro.png")
    
    # Se não tiver a clara, usa a escura (Mas vamos forçar o Invert agora)
    if not b64_light: 
        # st.toast("Aviso: Logo Claro não encontrado, usarei filtro de inversão.", icon="⚠️")
        b64_light = b64_dark
    # if not b64_dark: b64_dark = b64_light # Vice versa para garantir

    # 2. Injeta CSS com Variáveis CSS para imagens
    st.markdown(
        f"""
        <style>
            :root {{
                /* Configuração de Cores do Tema */
                --card-bg: var(--secondary-background-color);
                --card-border: var(--background-color);
                
                /* Usamos a MESMA imagem base (Escura/Branca) e invertemos via CSS se necessário */
                --img-logo-main: url('data:image/png;base64,{b64_dark}');
            }}
            
            /* --- LOGO ADAPTÁVEL (CSS FILTER MAGIC) --- */
            
            .logo-adaptive {{
                display: block;
                background-size: contain;
                background-repeat: no-repeat;
                background-position: center;
                /* Logo Padrão (Feito para Fundo Escuro -> Texto Branco) */
                background-image: var(--img-logo-main);
                transition: all 0.3s ease;
                filter: none; /* Normal */
            }}

            /* 2. REGRAS PARA MODO CLARO (LIGHT MODE) */
            /* Se o fundo for branco, aplicamos INVERT para tornar o Branco em Preto */
            
            /* Caso 1: Atributo data-theme na tag HTML ou BODY */
            html[data-theme="light"] .logo-adaptive,
            body[data-theme="light"] .logo-adaptive,
            /* Caso 2: Atributo no App Container (div principal do Streamlit) */
            [data-testid="stApp"][data-theme="light"] .logo-adaptive,
            /* Caso 3: Section main */
            section[data-testid="stMain"][data-theme="light"] .logo-adaptive,
            /* Caso 4: Qualquer pai com data-theme light */
            [data-theme="light"] .logo-adaptive {{
                /* Inverte as cores: Branco vira Preto, Amarelo vira Azul... */
                /* Ajustamos o brightness para garantir preto forte */
                filter: invert(1) brightness(0) !important; 
                opacity: 0.8 !important; /* Suavizar um pouco o preto absoluto */
            }}

            /* Caso 5: Preferência do Sistema (OS Light Mode) */
            /* Apenas se NÃO estiver forçado para dark no HTML */
            @media (prefers-color-scheme: light) {{
                html:not([data-theme="dark"]) .logo-adaptive,
                body:not([data-theme="dark"]) .logo-adaptive,
                [data-testid="stApp"]:not([data-theme="dark"]) .logo-adaptive {{
                     filter: invert(1) brightness(0) !important;
                     opacity: 0.8 !important;
                }}
            }}
        
            .yellow-header {{
                background-color: #FACC15;
                color: #0F172A;
                padding: 5px;
                border-radius: 5px 5px 0 0;
                text-align: center;
                font-weight: bold;
                margin-bottom: -5px;
                border: 1px solid var(--background-color);
                border-bottom: none;
            }}
            
            .kpi-card {{
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 12px;
                padding: 12px 14px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            
            .kpi-label {{
                color: var(--text-color);
                font-size: 12px;
                margin-bottom: 4px;
                letter-spacing: 0.3px;
                opacity: 0.8;
            }}
            
            .kpi-value {{
                color: var(--primary-color);
                font-size: 22px;
                font-weight: 700;
            }}
            
            .kpi-sub {{
                color: var(--text-color);
                font-size: 12px;
                opacity: 0.6;
            }}
            
            .toolbar {{
                display: flex;
                gap: 8px;
                align-items: center;
                justify-content: flex-end;
                margin-bottom: 10px;
            }}
            
            .toolbar-badge {{
                background: var(--secondary-background-color);
                color: var(--text-color);
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 12px;
                border: 1px solid var(--background-color);
            }}

            /* Sidebar Input Fix (opcional, só para garantir contorno suave) */
            section[data-testid="stSidebar"] .stTextInput > div > div {{
                border-radius: 8px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
