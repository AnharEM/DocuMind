import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>

/* --- Global Reset & Fonts --- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg-color: #000000;
    --card-bg: #000000;
    --text-primary: #FFFFFF;
    --text-secondary: #FFFFFF; 
    --border-color: #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
    background-color: var(--bg-color);
    font-size: 16px; 
    -webkit-font-smoothing: antialiased;
}

/* --- Animations --- */
@keyframes slideUpFade {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes logoPulse {
    0% { text-shadow: 0 0 5px rgba(255,255,255,0.1); }
    50% { text-shadow: 0 0 20px rgba(255,255,255,0.4), 0 0 30px rgba(255,255,255,0.1); }
    100% { text-shadow: 0 0 5px rgba(255,255,255,0.1); }
}

@keyframes lineExpand {
    0% { width: 0%; opacity: 0; }
    100% { width: 100%; opacity: 1; }
}

/* --- App Container --- */
.stApp {
    background-color: #000000;
    background-image: none;
    animation: slideUpFade 0.6s ease-out forwards;
}

/* --- UI Chrome Removal --- */
#MainMenu, footer, header {visibility: hidden;}

/* --- Sidebar --- */
[data-testid="stSidebar"] {
    background-color: #000000;
    border-right: 1px solid #333; /* Very subtle separation */
}

/* --- Cards (Modern Minimalist) --- */
.glass-card {
    background-color: #000000;
    border: 1px solid #333; /* Thin, subtle border */
    border-radius: 12px; /* Modern rounded corners */
    padding: 32px;
    margin-bottom: 24px;
    transition: transform 0.2s ease, border-color 0.2s ease;
    animation: slideUpFade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0; /* Starts hidden for animation */
}

/* Staggered animation delays for child cards if needed */
.stColumn:nth-child(1) .glass-card { animation-delay: 0.1s; }
.stColumn:nth-child(2) .glass-card { animation-delay: 0.2s; }
.stColumn:nth-child(3) .glass-card { animation-delay: 0.3s; }

.glass-card:hover {
    border-color: #FFFFFF; /* Highlight on hover */
    transform: translateY(-2px);
}

/* --- Typography --- */
h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    letter-spacing: -0.04em;
    font-size: 3.5rem !important;
    line-height: 1.1;
    color: #FFFFFF !important;
    margin-bottom: 1rem;
}

h2 {
    background-color: transparent;
    color: #FFFFFF !important;
    padding: 0;
    font-weight: 700;
    border: none;
    margin-top: 2rem;
    font-size: 1.5rem;
    letter-spacing: -0.02em;
    border-bottom: 1px solid #333;
    padding-bottom: 1rem;
    width: 100%;
    margin-bottom: 1rem;
}

h3 {
    font-weight: 600;
    color: #FFFFFF;
    border: none;
    padding-bottom: 0.5rem;
    margin-top: 1.5rem;
    font-size: 1.2rem;
}


p, li, label, .stMarkdown, .stText {
    color: #FFFFFF !important;
    line-height: 1.6;
    font-size: 1rem;
    opacity: 1 !important;
}

/* Fix for recursive opacity issues */
div {
    opacity: 1;
}

/* --- Buttons --- */
.stButton button {
    background-color: #000000;
    color: #FFFFFF;
    border: 1px solid #FFFFFF;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: all 0.2s ease;
}


.stButton button:hover {
    background-color: #000000;
    color: #FFFFFF;
    border-color: #FFFFFF;
    transform: translateY(-2px);
    box-shadow: 0 4px 0 #FFFFFF; /* Retro "Clicky" feel or just solid shadow */
}

.stButton button:active {
    transform: translateY(0);
    box-shadow: 0 0 0 #FFFFFF;
}

/* --- Inputs --- */
.stTextInput input {
    background-color: #000000;
    border: 1px solid #333;
    color: #FFFFFF;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    transition: border-color 0.2s;
}
.stTextInput input:focus {
    background-color: #000000;
    color: #FFFFFF;
    border-color: #FFFFFF;
    box-shadow: 0 0 0 1px #FFFFFF;
}

/* --- Tabs --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    border-bottom: 1px solid #333;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border: none;
    color: rgba(255,255,255,0.7); /* Improved visibility */
    font-weight: 500;
    border-radius: 0px;
    padding-bottom: 12px;
}
.stTabs [aria-selected="true"] {
    background-color: transparent !important;
    color: #FFFFFF !important;
    border-bottom: 2px solid #FFFFFF !important;
}

/* --- Alerts --- */
div[data-baseweb="notification"], .stAlert {
    background-color: #000000 !important;
    border: 1px solid #FFFFFF !important;
    color: #FFFFFF !important;
    border-radius: 8px;
}
/* Force Icons to White */
.stAlert > div > div > div > svg {
    fill: #FFFFFF !important;
}

/* --- Usage Bar --- */
.stProgress > div > div > div > div {
    background-color: #FFFFFF;
}

/* --- Spinner --- */
.stSpinner > div {
    border-top-color: #FFFFFF !important;
}

/* --- File Uploader Button Specifics --- */
[data-testid="stFileUploader"] {
    animation: slideUpFade 0.4s ease-out forwards;
}
[data-testid="stFileUploader"] section {
    border: 1px dashed #333 !important;
    border-radius: 12px !important;
    background: linear-gradient(180deg, rgba(25,25,25,0.5) 0%, rgba(0,0,0,0) 100%) !important;
    transition: border-color 0.3s ease;
    padding: 3rem 2rem !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #555 !important;
}
[data-testid="stFileUploader"] button {
    border-color: #333;
    color: #FFFFFF;
    background-color: #000000;
}
[data-testid="stFileUploader"] button:hover {
    border-color: #FFFFFF;
    color: #FFFFFF;
    background-color: #000000;
    box-shadow: 0 2px 0 #FFFFFF;
}

/* --- Scrollbars --- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #555; }
</style>
</style>
""", unsafe_allow_html=True)

def render_feature_card(title, description):
    # Brutalist Card
    st.markdown(f"""
<div class="glass-card">
    <h3 style="border:none; padding:0; margin:0; font-size: 1.4rem;">{title}</h3>
    <p style="opacity: 1; margin-top: 0.5rem;">{description}</p>
</div>
""", unsafe_allow_html=True)

def render_result_card(title, content, footer=""):
    footer_html = f'<div style="border-top: 2px solid #FFF; padding-top: 1rem; margin-top: 1rem; font-size: 0.9rem;">{footer}</div>' if footer else ""
    st.markdown(f"""
<div class="glass-card">
    <h2 style="margin-top:0; border:none; padding:0; background:transparent; color:#FFF !important; font-size:1.8rem;">{title}</h2>
    <div style="margin-top: 1rem; border-top: 1px solid #333; padding-top:1rem;">
        {content}
    </div>
    {footer_html}
</div>
""", unsafe_allow_html=True)
