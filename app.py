import streamlit as st
from groq import Groq

# Page Styling - Customized for Benedict College
st.set_page_config(page_title="BC TigerMath AI", page_icon="🐅", layout="centered")

# --- 🎨 Custom CSS Injection: BC Purple & Tiger Gold Theme ---
st.markdown("""
    <style>
    /* Title and Subtitle Styling */
    h1 {
        color: #FFD700 !important; /* Tiger Gold */
        font-family: 'Arial Black', Gadget, sans-serif;
    }
    .stCaption {
        color: #F0F2F6 !important;
        font-style: italic;
    }
    
    /* Custom Design for the Math Toolbar Buttons */
    div.stButton > button {
        background-color: #4C145E !important; /* BC Purple Background */
        color: #FFD700 !important; /* Tiger Gold Text */
        border: 2px solid #FFD700 !important;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #FFD700 !important; /* Invert on hover */
        color: #4C145E !important;
        border: 2px solid #4C145E !important;
    }
    
    /* Accent lines and styling wrappers */
    div[data-testid="stSidebar"] {
        background-color: #1A1A1A;
    }
    div[data-testid="stChatInput"] {
        border: 2px solid #4C145E !important;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================
# LANGUAGE CONFIGURATIONS
# =====================================
captions = {
    "English": "Your Campus BC Math Specialist | Created by Mark Wells and Jamazio Mcphee",
    "Español": "Tu Especialista Matemático BC | Creado por Mark Wells y Jamazio Mcphee",
    "Français": "Votre spécialiste mathématique BC | Créé par Mark Wells et Jamazio Mcphee"
}

LANGUAGE_PROMPT = {
    "English": "You MUST respond ONLY in English.",
    "Español": "Debes responder ÚNICAMENTE en español.",
    "Français": "Vous devez répondre UNIQUEMENT en français."
} 

# --- Initialize Local Chat History, Language & Input Buffers ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

# Dynamic header caption based on selected language
st.title("🐅 BC TigerMath AI")
st.caption(captions[st.session_state.language])

# --- Sidebar: Equation Builder & Control Panel ---
with st.sidebar:
    st.header("🧮 Equation Builder")
    st.caption("Build your expression here, then copy it to the chat!")
    
    # 1. Setup the session state for our equation builder
    if "equation_draft" not in st.session_state:
        st.session_state.equation_draft = ""

    # 2. Callbacks to modify the text input programmatically
    def add_symbol(sym):
        st.session_state.equation_draft += sym

    def clear_equation():
        st.session_state.equation_draft = ""

    # 3. Render the Composer Input Box and a Clear button
    draft_col, clear_col = st.columns([4, 1])
    with draft_col:
        st.text_input("Equation Composer:", key="equation_draft", label_visibility="collapsed")
    with clear_col:
        st.button("❌", on_click=clear_equation, use_container_width=True)

    # 4. Math Level Tabs
    math_tabs = st.tabs(["➕ Alg", "📈 Calc", "📊 Stat", "📐 Trig"])

    # Helper function to generate clean button grids
    def render_symbol_grid(symbols, prefix):
        cols = st.columns(4)
        for i, sym in enumerate(symbols):
            with cols[i % 4]:
                st.button(sym, key=f"{prefix}_sym_{i}", on_click=add_symbol, args=(sym,), use_container_width=True)

    with math_tabs[0]: # Algebra & Basic Math
        render_symbol_grid(['+', '-', '×', '÷', '=', '≠', 'x²', 'x³', 'xⁿ', '√', '∛', '()', '[]', '|x|', '∞', '½'], "alg")

    with math_tabs[1]: # Calculus
        render_symbol_grid(['∫', '∬', '∭', '∮', '∂', 'd/dx', 'lim', '∑', '∏', 'Δ', '∇', 'e', 'ln', 'log', 'dx', 'dy'], "calc")

    with math_tabs[2]: # Statistics
        render_symbol_grid(['μ', 'σ', 'σ²', 'x̄', 'p̂', 'χ²', 'ρ', 'Z', 'T', 'P()', 'E()', 'Var()', '∩', '∪', '!', '≈'], "stat")

    with math_tabs[3]: # Trig & Sets
        render_symbol_grid(['π', 'θ', 'α', 'β', 'γ', 'sin', 'cos', 'tan', '∈', '∉', '⊂', '⊆', 'Ø', '°', '∠', '△'], "trig")

    st.write("---")
    
    # --- Control Panel & Language Configuration ---
    st.header("Control Panel")
    st.info("The BC Math Specialist is fully authenticated and ready to assist!")
    
    st.radio(
        "🌍 Choose Language",
        ["English", "Español", "Français"],
        key="language"
    )
    st.success(f"Current Language: {st.session_state.language}")
    
    st.write
