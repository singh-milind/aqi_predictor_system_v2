import streamlit as st
import streamlit.components.v1 as components

def inject_glassmorphism():
    css = """
    <style>
        /* Import Modern Font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
        
        /* Apply Font */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
        }

        /* App Background (Black with subtle glowing orbs) */
        .stApp {
            background-color: #050505 !important;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(56, 189, 248, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(232, 121, 249, 0.15), transparent 25%) !important;
            background-attachment: fixed !important;
            color: #f8fafc !important;
        }

        /* AGGRESSIVE OVERRIDES: Hide Streamlit Defaults */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        footer {
            display: none !important;
        }
        .stDeployButton {
            display: none !important;
        }
        
        /* Fix padding to make it a true web app */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }

        /* Nav Buttons styled as Segmented Pills */
        div[data-testid="stHorizontalBlock"] button {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 50px !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stHorizontalBlock"] button:hover {
            background: rgba(255, 255, 255, 0.15) !important;
            color: #fff !important;
            border-color: #38bdf8 !important;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
        }

        /* TRUE Glassmorphism Containers - Matched to .custom-card */
        [data-testid="stVerticalBlockBorderWrapper"],
        div[style*="border-radius: 0.5rem"][style*="border: 1px solid"],
        div.st-emotion-cache-1kyxreq,
        div.st-emotion-cache-1r6slb0 {
            background-color: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 20px !important;
            padding: 2rem !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
            margin-bottom: 20px !important;
        }
        
        /* Match Subheaders inside bordered containers to .card-label */
        [data-testid="stVerticalBlockBorderWrapper"] h3,
        div[style*="border-radius: 0.5rem"][style*="border: 1px solid"] h3 {
            font-size: 1.1rem !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            background: none !important;
            -webkit-text-fill-color: initial !important;
            margin-bottom: 1.5rem !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding-bottom: 0.5rem !important;
        }

        /* Slider Customization */
        div[data-testid="stSlider"] div[role="slider"] {
            background: #38bdf8 !important;
            box-shadow: 0 0 10px #38bdf8 !important;
            border: 2px solid #fff !important;
        }
        
        /* Primary Action Buttons (Predict / Simulate) */
        button[kind="primary"] {
            background: linear-gradient(90deg, #38bdf8, #818cf8) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            padding: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 10px 20px rgba(56, 189, 248, 0.3) !important;
        }
        button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 25px rgba(56, 189, 248, 0.5) !important;
        }

        /* Headers with glowing gradient */
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #38bdf8, #e879f9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            letter-spacing: -1px;
        }
        
        /* Custom Raw HTML Card Classes */
        .custom-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            flex-direction: column;
            gap: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }
        .card-label {
            font-size: 0.9rem;
            color: #94a3b8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .card-value {
            font-size: 3rem;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }
        .card-subtext {
            font-size: 0.85rem;
            color: #64748b;
        }
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .status-safe { background: rgba(76, 175, 80, 0.2); color: #4CAF50; border: 1px solid #4CAF50; }
        .status-warn { background: rgba(255, 152, 0, 0.2); color: #FF9800; border: 1px solid #FF9800; }
        .status-danger { background: rgba(244, 67, 54, 0.2); color: #F44336; border: 1px solid #F44336; }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def style_container(marker_id):
    """
    Injects Javascript to dynamically find the parent bordered container of a marker
    and applies the exact .custom-card aesthetic to it. This bypasses Streamlit CSS limitations.
    """
    js = f"""
    <script>
        // Use a small delay to ensure the DOM is fully rendered
        setTimeout(function() {{
            const marker = window.parent.document.getElementById('{marker_id}');
            if (marker) {{
                // Find the parent div that has the Streamlit border wrapper class
                let container = marker.closest('div[data-testid="stVerticalBlockBorderWrapper"]');
                
                // Fallback: traverse up and find the first div with a border radius style
                if (!container) {{
                    let parent = marker.parentElement;
                    while (parent && parent.tagName === 'DIV') {{
                        if (parent.style.borderRadius === '0.5rem') {{
                            container = parent;
                            break;
                        }}
                        parent = parent.parentElement;
                    }}
                }}
                
                if (container) {{
                    // Apply the .custom-card aesthetic directly via inline styles
                    container.style.setProperty('background-color', 'rgba(255, 255, 255, 0.03)', 'important');
                    container.style.setProperty('border', '1px solid rgba(255, 255, 255, 0.08)', 'important');
                    container.style.setProperty('border-radius', '20px', 'important');
                    container.style.setProperty('box-shadow', '0 10px 30px rgba(0,0,0,0.5)', 'important');
                    container.style.setProperty('padding', '2rem', 'important');
                }}
            }}
        }}, 100);
    </script>
    """
    components.html(js, height=0, width=0)

