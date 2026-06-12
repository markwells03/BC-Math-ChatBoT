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
    </style>
""", unsafe_allow_html=True)

st.title("🐅 BC TigerMath AI")
st.caption("Your Campus BC Math Specialist | Created by Mark Wells and Jamazio Mcphee")

# --- Setup Global States ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# --- Callback Functions ---
def add_symbol(sym):
    st.session_state.user_input += sym

def set_quick_prompt(text):
    st.session_state.user_input = text

def reset_chat():
    st.session_state.messages = []
    st.session_state.user_input = ""

# --- Sidebar: Equation Builder & Control Panel ---
with st.sidebar:
    st.header("🧮 Equation Builder")
    st.caption("Clicking these symbols will instantly type them into your chat box!")
    
    # Math Level Tabs 
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
    
    # Standard Control Panel 
    st.header("Control Panel")
    st.info("The BC Math Specialist is fully authenticated and ready to assist!")
    st.button("Reset Conversation", on_click=reset_chat, use_container_width=True)

# --- 1. Render Existing Chat Thread ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 2. Interactive UI Tools (Always Anchored Cleanly at the Bottom) ---
st.write("---")
st.markdown("**Quick-Load Problem Starters:**")
col1, col2, col3, col4 = st.columns(4)

col1.button("➕ Algebra Setup", on_click=set_quick_prompt, args=("How do I solve a quadratic equation like x² - 5x + 6 = 0?",), use_container_width=True)
col2.button("📐 Pre-Calc Help", on_click=set_quick_prompt, args=("Can you help me find the exact value of sin(π/3)?",), use_container_width=True)
col3.button("📈 Calculus Rules", on_click=set_quick_prompt, args=("I need help finding the derivative of f(x) = x² * e^x.",), use_container_width=True)
col4.button("📊 Stats & Data", on_click=set_quick_prompt, args=("How do I calculate the standard deviation or z-score of a dataset?",), use_container_width=True)

# Custom Chat Input Box Setup
# We use a form here to completely stop accidental submissions when clicking options!
with st.form(key="chat_form", clear_on_submit=False):
    input_col, btn_col = st.columns([6, 1])
    with input_col:
        user_query = st.text_input("Ask a question...", key="user_input", label_visibility="collapsed")
    with btn_col:
        submit_clicked = st.form_submit_button("Send", use_container_width=True)

# --- 3. Handle Form Submission Processing Layer ---
if submit_clicked and user_query.strip() != "":
    
    # Add user message to history and show it
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # Clear out input state for next input round
    st.session_state.user_input = ""
        
    try:
        with open("benedict_info.txt", "r", encoding="utf-8") as file:
            campus_kb = file.read()
    except FileNotFoundError:
        campus_kb = "No supplementary historical documents found."

    SYSTEM_INSTRUCTION = f"""You are 'BC TigerMath AI', a strict Socratic mathematics tutor and the premier BC Math Specialist at Benedict College. Match the energy a person comes with, and add a little tiger pride and humor from time to time.

    🔴 CAMPUS KNOWLEDGE EXCEPTION:
    - If the user asks general questions about Benedict College, step out of math mode entirely and answer directly using ONLY the data below.

    📋 VERIFIED CAMPUS DATA FROM REPOSITORY:
    {campus_kb}

    📐 MATHEMATICS DIRECTIVES:
    - NEVER give the user the final solution or write out a complete step-by-step answer upfront. Your core job is to guide them using the Socratic method.
    - Provide ONE small hint or ask ONE target question at a time.
    - Keep responses to a few sentences max.
    """
    
    formatted_messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for msg in st.session_state.messages[:-1]: 
        formatted_messages.append({"role": msg["role"], "content": msg["content"]})
    formatted_messages.append({"role": "user", "content": user_query})
        
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
            st.error(f"Authentication or API Error.")
            st.info(str(e))
            
    st.rerun()
