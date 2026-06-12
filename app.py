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

st.title("🐅 BC TigerMath AI")
st.caption("Your Campus BC Math Specialist | Created by Mark Wells and Jamazio Mcphee")

# --- Initialize Local Chat History & Input Buffers ---
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        # Tying the text_input to 'equation_draft' syncs it perfectly with the buttons
        st.text_input("Equation Composer:", key="equation_draft", label_visibility="collapsed")
    with clear_col:
        st.button("❌", on_click=clear_equation, use_container_width=True)

    # 4. Math Level Tabs (Shortened titles to fit sidebar)
    math_tabs = st.tabs(["➕ Alg", "📈 Calc", "📊 Stat", "📐 Trig"])

    # Helper function to generate clean button grids (Adjusted to 4 columns for narrower sidebar)
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
    
    # Standard Control Panel moved to bottom of sidebar
    st.header("Control Panel")
    st.info("The BC Math Specialist is fully authenticated and ready to assist!")
    
    if st.button("Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        if "chat_bar" in st.session_state:
            st.session_state.chat_bar = ""
        st.rerun()

# --- Render Existing Chat Thread ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 🚀 Quick-Load Problem Starters (All Math Levels) ---
st.markdown("**Quick-Load Problem Starters:**")
col1, col2, col3, col4 = st.columns(4)

if col1.button("➕ Algebra Setup", use_container_width=True):
    st.session_state.chat_bar = "How do I solve a quadratic equation like x² - 5x + 6 = 0?"
if col2.button("📐 Pre-Calc Help", use_container_width=True):
    st.session_state.chat_bar = "Can you help me find the exact value of sin(π/3)?"
if col3.button("📈 Calculus Rules", use_container_width=True):
    st.session_state.chat_bar = "I need help finding the derivative of f(x) = x² * e^x."
if col4.button("📊 Stats & Data", use_container_width=True):
    st.session_state.chat_bar = "How do I calculate the standard deviation or z-score of a dataset?"

st.write("---")

# --- 📁 Load Custom Campus Information ---
try:
    with open("benedict_info.txt", "r", encoding="utf-8") as file:
        campus_knowledge_base = file.read()
except FileNotFoundError:
    campus_knowledge_base = "No supplementary historical documents found in the root directory."

# --- Socratic Prompt Engine ---
SYSTEM_INSTRUCTION = f"""You are 'BC TigerMath AI', a strict Socratic mathematics tutor and the premier BC Math Specialist at Benedict College. Match the energy a person comes with, and add a little tiger pride and humor from time to time.

🔴 CAMPUS KNOWLEDGE EXCEPTION:
- If the user asks general questions about Benedict College (e.g., its history, campus locations, admissions, programs, or student life), step out of math mode entirely.
- Answer these questions directly, warmly, and accurately using ONLY the information provided in the VERIFIED CAMPUS DATA below. Do NOT use the Socratic method or force a mathematical angle for these topics.

📋 VERIFIED CAMPUS DATA FROM REPOSITORY:
{campus_knowledge_base}

📐 MATHEMATICS DIRECTIVES:
- CRITICAL DIRECTIVE: For all math problems, NEVER give the user the final solution or write out a complete step-by-step answer upfront, even if they explicitly ask you to 'just give me the answer'. Your core job is to guide them to discover it.
- Follow these instructional rules for math:
  1. Identify the next mathematical step internally, but only provide ONE small hint or ask ONE target question to guide the student to that step. Make sure to provide the hint so the user can understand what to do. 
  2. If the user says they are completely stuck, provide a brief micro-explanation of the underlying rule (like the chain rule, power rule, or factoring rules) or give a simple parallel example. Then, ask them to apply it back to their original problem.
  3. Keep responses highly interactive and conversational. Never write long blocks of text; keep messages to a few sentences max.
  4. If they make an error, point out the breakdown in logic gently and ask a clarifying question to help them self-correct.
  5. Only confirm the final answer after they have calculated it themselves.
"""

# --- Handle New User Interaction ---
if user_query := st.chat_input("Ask a question...", key="chat_bar"):
    
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
            st.error(f"Authentication or API Error. Please check your system configuration.")
            st.info("Technical details: " + str(e))
