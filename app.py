import streamlit as st
from groq import Groq

# --- 1. Page Styling & Config ---
st.set_page_config(page_title="BC TigerMath AI", page_icon="🐅", layout="wide")

st.markdown("""
    <style>
    /* Title and Subtitle Styling */
    h1 { color: #FFD700 !important; font-family: 'Arial Black', Gadget, sans-serif; }
    .stCaption { color: #F0F2F6 !important; font-style: italic; }
    
    /* Custom Design for the Math Toolbar Buttons */
    div.stButton > button {
        background-color: #4C145E !important; 
        color: #FFD700 !important; 
        border: 2px solid #FFD700 !important;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #FFD700 !important; 
        color: #4C145E !important;
        border: 2px solid #4C145E !important;
    }
    
    /* Accent lines and styling wrappers */
    div[data-testid="stSidebar"] { background-color: #1A1A1A; }
    div[data-testid="stChatInput"] { border: 2px solid #4C145E !important; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. Multi-Language UI Dictionary ---
UI_TEXT = {
    "English": {
        "caption": "Your Campus Benedict Math Specialist | Created by Mark Wells and Jamazio Mcphee",
        "lang_prompt": "🌍 Select Your Language",
        "eq_header": "🧮 Equation Builder",
        "eq_caption": "Build your expression here, then copy it to the chat!",
        "eq_composer": "Equation Composer:",
        "ctrl_header": "Control Panel",
        "ctrl_info": "The BC Math Specialist is authenticated and ready to assist!",
        "reset_btn": "Reset Conversation",
        "quick_title": "**Quick-Load Problem Starters:**",
        "ql_1_btn": "➕ Algebra Setup",
        "ql_1_msg": "How do I solve a quadratic equation like x² - 5x + 6 = 0?",
        "ql_2_btn": "📐 Pre-Calc Help",
        "ql_2_msg": "Can you help me find the exact value of sin(π/3)?",
        "ql_3_btn": "📈 Calculus Rules",
        "ql_3_msg": "I need help finding the derivative of f(x) = x² * e^x.",
        "ql_4_btn": "📊 Stats & Data",
        "ql_4_msg": "How do I calculate the standard deviation or z-score of a dataset?",
        "chat_placeholder": "Hi there! What math problem can I help you with today? 🐅", # <--- UPDATED HERE
        "sys_prompt": "You MUST respond ONLY in English.",
        "error_msg": "Authentication or API Error. Please check your system configuration."
    },
    "Español": {
        "caption": "Tu Especialista Matemático BC | Creado por Mark Wells y Jamazio Mcphee",
        "lang_prompt": "🌍 Selecciona tu idioma",
        "eq_header": "🧮 Creador de Ecuaciones",
        "eq_caption": "¡Construye tu expresión aquí, luego cópiala al chat!",
        "eq_composer": "Compositor de Ecuaciones:",
        "ctrl_header": "Panel de Control",
        "ctrl_info": "¡El Especialista Matemático BC está listo para ayudar!",
        "reset_btn": "Reiniciar Conversación",
        "quick_title": "**Iniciadores de Problemas Rápidos:**",
        "ql_1_btn": "➕ Álgebra",
        "ql_1_msg": "¿Cómo resuelvo una ecuación cuadrática como x² - 5x + 6 = 0?",
        "ql_2_btn": "📐 Pre-Cálculo",
        "ql_2_msg": "¿Puedes ayudarme a encontrar el valor exacto de sin(π/3)?",
        "ql_3_btn": "📈 Cálculo",
        "ql_3_msg": "Necesito ayuda para encontrar la derivada de f(x) = x² * e^x.",
        "ql_4_btn": "📊 Estadística",
        "ql_4_msg": "¿Cómo calculo la desviación estándar o el valor z de un conjunto de datos?",
        "chat_placeholder": "¡Hola! ¿Con qué problema de matemáticas te puedo ayudar hoy? 🐅", # <--- UPDATED HERE
        "sys_prompt": "Debes responder ÚNICAMENTE en español.",
        "error_msg": "Error de API o autenticación. Verifica la configuración de tu sistema."
    },
    "Français": {
        "caption": "Votre spécialiste mathématique BC | Créé par Mark Wells et Jamazio Mcphee",
        "lang_prompt": "🌍 Choisissez votre langue",
        "eq_header": "🧮 Créateur d'Équations",
        "eq_caption": "Construisez votre expression ici, puis copiez-la dans le chat !",
        "eq_composer": "Compositeur d'Équations :",
        "ctrl_header": "Panneau de Configuration",
        "ctrl_info": "Le spécialiste mathématique BC est prêt à vous aider !",
        "reset_btn": "Réinitialiser la Conversation",
        "quick_title": "**Démarreurs Rapides de Problèmes :**",
        "ql_1_btn": "➕ Algèbre",
        "ql_1_msg": "Comment résoudre une équation quadratique comme x² - 5x + 6 = 0 ?",
        "ql_2_btn": "📐 Pré-Calcul",
        "ql_2_msg": "Pouvez-vous m'aider à trouver la valeur exacte de sin(π/3) ?",
        "ql_3_btn": "📈 Calcul",
        "ql_3_msg": "J'ai besoin d'aide pour trouver la dérivée de f(x) = x² * e^x.",
        "ql_4_btn": "📊 Statistiques",
        "ql_4_msg": "Comment calculer l'écart type ou le score z d'un ensemble de données ?",
        "chat_placeholder": "Bonjour ! Avec quel problème de mathématiques puis-je vous aider aujourd'hui ? 🐅", # <--- UPDATED HERE
        "sys_prompt": "Vous devez répondre UNIQUEMENT en français.",
        "error_msg": "Erreur d'authentification ou d'API. Veuillez vérifier votre configuration."
    }
}

# --- 3. Initialize Session State Variables ---
if "language" not in st.session_state:
    st.session_state.language = "English"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "equation_draft" not in st.session_state:
    st.session_state.equation_draft = ""
if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None  # Safely handles button clicks

# Load active language dictionary
lang = UI_TEXT[st.session_state.language]

# --- 4. Sidebar: Language Prompt, Equation Builder & Control Panel ---
with st.sidebar:
    # Prominent Language Selector
    st.radio(
        lang["lang_prompt"],
        ["English", "Español", "Français"],
        key="language" # Triggers instant page rerun and updates UI dictionary
    )
    st.write("---")
    
    st.header(lang["eq_header"])
    st.caption(lang["eq_caption"])
    
    def add_symbol(sym): st.session_state.equation_draft += sym
    def clear_equation(): st.session_state.equation_draft = ""

    draft_col, clear_col = st.columns([4, 1])
    with draft_col:
        st.text_input(lang["eq_composer"], key="equation_draft", label_visibility="collapsed")
    with clear_col:
        st.button("❌", on_click=clear_equation, use_container_width=True)

    math_tabs = st.tabs(["➕ Alg", "📈 Calc", "📊 Stat", "📐 Trig"])

    def render_symbol_grid(symbols, prefix):
        cols = st.columns(4)
        for i, sym in enumerate(symbols):
            with cols[i % 4]:
                st.button(sym, key=f"{prefix}_sym_{i}", on_click=add_symbol, args=(sym,), use_container_width=True)

    with math_tabs[0]: render_symbol_grid(['+', '-', '×', '÷', '=', '≠', 'x²', 'x³', 'xⁿ', '√', '∛', '()', '[]', '|x|', '∞', '½'], "alg")
    with math_tabs[1]: render_symbol_grid(['∫', '∬', '∭', '∮', '∂', 'd/dx', 'lim', '∑', '∏', 'Δ', '∇', 'e', 'ln', 'log', 'dx', 'dy'], "calc")
    with math_tabs[2]: render_symbol_grid(['μ', 'σ', 'σ²', 'x̄', 'p̂', 'χ²', 'ρ', 'Z', 'T', 'P()', 'E()', 'Var()', '∩', '∪', '!', '≈'], "stat")
    with math_tabs[3]: render_symbol_grid(['π', 'θ', 'α', 'β', 'γ', 'sin', 'cos', 'tan', '∈', '∉', '⊂', '⊆', 'Ø', '°', '∠', '△'], "trig")

    st.write("---")
    
    st.header(lang["ctrl_header"])
    st.info(lang["ctrl_info"])
    
    if st.button(lang["reset_btn"], use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. Main Content Area ---
st.title("🐅 BC TigerMath AI")
st.caption(lang["caption"])

# --- 6. Quick-Load Problem Starters (Safe Implementation) ---
st.markdown(lang["quick_title"])
col1, col2, col3, col4 = st.columns(4)

# Instead of modifying the chat input widget state, we store the prompt in a temp variable
if col1.button(lang["ql_1_btn"], use_container_width=True): st.session_state.quick_prompt = lang["ql_1_msg"]
if col2.button(lang["ql_2_btn"], use_container_width=True): st.session_state.quick_prompt = lang["ql_2_msg"]
if col3.button(lang["ql_3_btn"], use_container_width=True): st.session_state.quick_prompt = lang["ql_3_msg"]
if col4.button(lang["ql_4_btn"], use_container_width=True): st.session_state.quick_prompt = lang["ql_4_msg"]

st.write("---")

# --- 7. Load Custom Campus Information ---
try:
    with open("benedict_info.txt", "r", encoding="utf-8") as file:
        campus_knowledge_base = file.read()
except FileNotFoundError:
    campus_knowledge_base = "No supplementary historical documents found in the root directory."

# --- 8. Construct Socratic Prompt ---
SYSTEM_INSTRUCTION = f"""You are 'BC TigerMath AI', a strict Socratic mathematics tutor and the premier BC Math Specialist at Benedict College. Match the energy a person comes with, and add a little tiger pride and humor from time to time.

CRITICAL LANGUAGE REQUIREMENT:
{lang["sys_prompt"]} Everything you output must strictly match this language constraint.

🔴 CAMPUS KNOWLEDGE EXCEPTION:
- If the user asks general questions about Benedict College, step out of math mode entirely.
- Answer these questions accurately using ONLY the information provided in the VERIFIED CAMPUS DATA below. Do NOT use the Socratic method for these topics.

📋 VERIFIED CAMPUS DATA FROM REPOSITORY:
{campus_knowledge_base}

📐 MATHEMATICS DIRECTIVES:
- CRITICAL DIRECTIVE: For all math problems, NEVER give the user the final solution or write out a complete step-by-step answer upfront. Your core job is to guide them to discover it.
  1. Identify the next mathematical step internally, but only provide ONE small hint or ask ONE target question to guide the student.
  2. If the user says they are completely stuck, provide a brief micro-explanation of the underlying rule.
  3. Keep responses highly interactive and conversational. Never write long blocks of text.
  4. If they make an error, point out the breakdown in logic gently.
  5. Only confirm the final answer after they have calculated it themselves.
"""

# --- 9. Render Existing Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 10. Handle Input (Chat Box OR Quick Load Buttons) ---
# Determine where the query is coming from
user_query = st.chat_input(lang["chat_placeholder"])

# If a quick-load button was pressed, override the empty chat_input with the button's message
if st.session_state.quick_prompt:
    user_query = st.session_state.quick_prompt
    st.session_state.quick_prompt = None # Reset the trigger

# Process the query
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    formatted_messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for msg in st.session_state.messages:
        formatted_messages.append({"role": msg["role"], "content": msg["content"]})
        
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            response_stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=formatted_messages,
                temperature=0.6,
                stream=True
            )
            
            for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
                    
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(lang["error_msg"])
            st.info("Technical details: " + str(e))
