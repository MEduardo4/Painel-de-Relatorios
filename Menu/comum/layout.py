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
            # print(f"DEBUG: Tenting load image from: {img_path}")
            with open(img_path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
                # print(f"DEBUG: Loaded {len(data)} bytes for {filename}")
                return data
        except Exception as e:
            print(f"DEBUG ERROR loading {filename}: {e}")
            return ""

    b64_dark = get_b64("Logo_BRG.png")
    b64_light = get_b64("Logo_BRGTemaClaro.png") # Agora obrigatório a imagem clara existir

    # Se falhar, duplicar a escura
    if not b64_light: b64_light = b64_dark
    if not b64_dark: b64_dark = b64_light

    # SVG Inline com CSS interno para preencher e trocar
    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 500 150" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="adaptive-svg-logo">
    <style>
        /* Padrão para SVG */
        .logo-img-dark {{ display: block; }}
        .logo-img-light {{ display: none; }}
        
        /* Detecção de Sistema Operacional */
        @media (prefers-color-scheme: light) {{
            .logo-img-dark {{ display: none; }}
            .logo-img-light {{ display: block; }}
        }}
    </style>
    <!-- Imagem Escura (Default) -->
    <image href="data:image/png;base64,{b64_dark}" xlink:href="data:image/png;base64,{b64_dark}" width="500" height="150" class="logo-img-dark" />
    <!-- Imagem Clara -->
    <image href="data:image/png;base64,{b64_light}" xlink:href="data:image/png;base64,{b64_light}" width="500" height="150" class="logo-img-light" />
</svg>"""
    return svg

def inject_styles():
    # Injeta apenas o CSS global que controla as classes do SVG
    st.markdown(
        """
        <style>
            :root {
                --card-bg: var(--secondary-background-color);
                --card-border: var(--background-color);
            }
            
            /* --- CONTROLE DO SVG VIA CSS GLOBAL DO STREAMLIT --- */
            /* Isso garante que a troca de tema do menu Settings funcione */
            
            /* Se o TEMA for LIGHT... */
            [data-theme="light"] .adaptive-svg-logo .logo-img-dark,
            section[data-theme="light"] .adaptive-svg-logo .logo-img-dark,
            body.detected-light .adaptive-svg-logo .logo-img-dark {
                display: none !important;
            }
            
            [data-theme="light"] .adaptive-svg-logo .logo-img-light,
            section[data-theme="light"] .adaptive-svg-logo .logo-img-light,
            body.detected-light .adaptive-svg-logo .logo-img-light {
                display: block !important;
            }
            
            /* ------------------------------------------------ */
            /* --- ESTILOS GERAIS (Recuperados) --- */
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

            /* Sidebar Input Fix */
            section[data-testid="stSidebar"] .stTextInput > div > div {
                border-radius: 8px;
            }
            
            /* 3. CLASSE FORÇADA VIA JS (Detected Light) */
            body.detected-light .logo-adaptive,
            .detected-light .logo-adaptive {
                background-image: var(--img-logo-light) !important;
            }
        </style>
        
        <script>
            // SCRIPT SENSOR DE TEMA (BASEADO EM VARIÁVEIS DO STREAMLIT)
            // O Streamlit injeta a variável --text-color no Iframe.
            // Se o texto for escuro (#31333F ou preto), o fundo é claro (Light Mode).
            // Se o texto for claro (branco), o fundo é escuro (Dark Mode).
            
            function detectStreamlitTheme() {
                const body = document.body;
                // Pega o valor computado da variável CSS --text-color
                const style = getComputedStyle(body);
                // Tenta pegar --text-color (padrão streamlit) ou fallback para color
                let textColor = style.getPropertyValue('--text-color').trim();
                
                // Se não encontrar a variável (raro), pega a cor computada do corpo
                if (!textColor) {
                    textColor = style.color;
                }
                
                // Função auxiliar para saber se a cor é escura (brightness)
                function isColorDark(colorString) {
                    // Converte cores nomeadas ou hex para RGB se necessário (simplificado)
                    // Streamlit geralmente retorna hex (#31333F) ou rgb.
                    
                    if (colorString.startsWith('#')) {
                        const hex = colorString.substring(1);
                        const r = parseInt(hex.substr(0, 2), 16);
                        const g = parseInt(hex.substr(2, 2), 16);
                        const b = parseInt(hex.substr(4, 2), 16);
                        // Fórmula de brilho (YIQ)
                        return ((r * 299) + (g * 587) + (b * 114)) / 1000 < 128;
                    } else if (colorString.startsWith('rgb')) {
                        const rgb = colorString.match(/\d+/g);
                        if(rgb) {
                            const r = parseInt(rgb[0]);
                            const g = parseInt(rgb[1]);
                            const b = parseInt(rgb[2]);
                            return ((r * 299) + (g * 587) + (b * 114)) / 1000 < 128;
                        }
                    }
                    return true; // Default assume escuro se falhar
                }
                
                const textIsDark = isColorDark(textColor);
                console.log("Theme Sensor: Text Color =", textColor, "Is Dark? =", textIsDark, "-> Mode:", textIsDark ? "LIGHT" : "DARK");
                
                // LÓGICA: Se o texto é escuro, o TEMA É CLARO.
                if (textIsDark) {
                    if (!body.classList.contains('detected-light')) {
                        console.log("Adding detected-light class");
                        body.classList.add('detected-light');
                    }
                } else {
                    if (body.classList.contains('detected-light')) {
                        console.log("Removing detected-light class");
                        body.classList.remove('detected-light');
                    }
                }
            }
            
            // Roda imediatamente
            detectStreamlitTheme();
            // Roda periodicamente (para pegar a troca feita no menu Settings)
            setInterval(detectStreamlitTheme, 1000);
        </script>
        """,
        unsafe_allow_html=True,
    )
