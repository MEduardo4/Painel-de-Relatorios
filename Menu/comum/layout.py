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


# Função auxiliar para gerar SVG inline com as duas imagens embutidas
def get_adaptive_logo_svg(width="100%", height="auto"):
    import os
    import base64

    def get_b64(filename):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__)) 
            menu_dir = os.path.dirname(current_dir) 
            img_path = os.path.join(menu_dir, "images", filename)
            with open(img_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except:
            return ""

    b64_dark = get_b64("Logo_BRG.png")
    b64_light = get_b64("Logo_BRGTemaClaro.png") # Agora obrigatório a imagem clara existir
    
    import streamlit as st
    
    # 1. Tenta detectar tema via Python (Server-Side) para render inicial correta
    initial_theme = "dark"
    try:
        # Streamlit >= 1.40 usa st.context.theme
        theme_obj = getattr(st, "context", None) and getattr(st.context, "theme", None)
        if theme_obj:
            # Tenta atributos conhecidos (.base ou .type)
            initial_theme = getattr(theme_obj, "base", getattr(theme_obj, "type", "dark"))
    except:
        pass

    # Define classe inicial baseada no contexto do Python
    initial_class = "ctx-light" if initial_theme == "light" else "ctx-dark"

    # Validar unidades para CSS (adicionar px se for apenas número)
    if str(width).isdigit(): width = f"{width}px"
    if str(height).isdigit(): height = f"{height}px"

    # CSS Background Image approach (More robust)
    # Estratégia:
    # 1. ctx-light/dark: Definido pelo Python (estado inicial)
    # 2. detected-light/dark: Definido pelo JS (mudança dinâmica sem rerun)
    
    html = f"""
<style>
    .adaptive-logo-container {{
        width: {width};
        height: {height};
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        transition: background-image 0.3s ease-in-out;
    }}
    
    /* Default / Dark Base */
    .adaptive-logo-container {{ background-image: url('data:image/png;base64,{b64_dark}'); }}
    
    /* Server-Side State (Python Context) */
    .adaptive-logo-container.ctx-light {{ background-image: url('data:image/png;base64,{b64_light}'); }}
    .adaptive-logo-container.ctx-dark  {{ background-image: url('data:image/png;base64,{b64_dark}'); }}
    
    /* Client-Side Overrides (JS Sensor - !important para vencer o Python se houver drift) */
    body.detected-light .adaptive-logo-container {{ 
        background-image: url('data:image/png;base64,{b64_light}') !important; 
    }}
    body.detected-dark .adaptive-logo-container {{ 
        background-image: url('data:image/png;base64,{b64_dark}') !important; 
    }}
    
    /* Media Query Fallback (OS preference) */
    @media (prefers-color-scheme: light) {{
        .adaptive-logo-container:not(.ctx-dark) {{
            background-image: url('data:image/png;base64,{b64_light}');
        }}
    }}
</style>
<div class="adaptive-logo-container {initial_class}"></div>
"""
    return html

def inject_styles():
    # Injeta apenas o CSS global (KPIs, Badges) e o Script Sensor de Tema
    
    st.markdown(
        """
        <style>
            /* 1. ESTILOS GERAIS */
            :root {
                --card-bg: var(--secondary-background-color);
                --card-border: var(--background-color);
            }
            
            /* Hide Streamlit Header Anchors (Chain Icon) */
            h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
                display: none !important;
            }
            [data-testid="stHeaderActionElements"] {
                display: none !important;
            }
            
            [data-testid="stSidebar"] {
                background-color: var(--secondary-background-color);
            }
            
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            
            /* 2. BADGES & LABELS */
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
            
            .sidebar-badge {
                background: #FF4B4B;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                margin-left: auto;
            }
            
            .sidebar-badge.neutral {
                background: #777;
            }
            
            .last-updated {
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

            section[data-testid="stSidebar"] .stTextInput > div > div {
                border-radius: 8px;
            }
        </style>
        
        <script>
            // SCRIPT SENSOR DE TEMA (ROBUSTO)
            // Monitora mudanças para alternar classes no body
            
            function updateThemeClass() {
                const body = document.body;
                
                // Detecção via cor do texto
                const style = getComputedStyle(body);
                let textColor = style.getPropertyValue('--text-color').trim();
                if (!textColor) textColor = style.color;
                
                // Função de brilho
                function isColorDark(colorStr) {
                    if (colorStr.startsWith('#')) {
                        const hex = colorStr.substring(1);
                        const r = parseInt(hex.substr(0, 2), 16);
                        const g = parseInt(hex.substr(2, 2), 16);
                        const b = parseInt(hex.substr(4, 2), 16);
                        return ((r * 299) + (g * 587) + (b * 114)) / 1000 < 128;
                    } else if (colorStr.startsWith('rgb')) {
                        const rgb = colorStr.match(/\d+/g);
                        if(rgb && rgb.length >= 3) {
                            return ((parseInt(rgb[0]) * 299) + (parseInt(rgb[1]) * 587) + (parseInt(rgb[2]) * 114)) / 1000 < 128;
                        }
                    }
                    return true; // Default Dark
                }
                
                const textIsDark = isColorDark(textColor);

                if (textIsDark) {
                    // LIGHT MODE DETECTADO
                    if (!body.classList.contains('detected-light')) {
                        body.classList.add('detected-light');
                    }
                    if (body.classList.contains('detected-dark')) {
                        body.classList.remove('detected-dark');
                    }
                } else {
                    // DARK MODE DETECTADO
                    if (!body.classList.contains('detected-dark')) {
                        body.classList.add('detected-dark');
                    }
                    if (body.classList.contains('detected-light')) {
                        body.classList.remove('detected-light');
                    }
                }
            }

            // Executa imediatamente e periodicamente
            updateThemeClass();
            setInterval(updateThemeClass, 1000);
            
            const observer = new MutationObserver(function(mutations) {
                updateThemeClass();
            });
            observer.observe(document.body, { attributes: true, attributeFilter: ['class', 'style', 'data-theme'] });
        </script>
        """,
        unsafe_allow_html=True,
    )
