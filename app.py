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

# --- Sidebar: Cleaned Up Control Panel ---
with st.sidebar:
    st.header("Control Panel")
    st.info("The BC Math Specialist is fully authenticated and ready to assist!")
    
    st.write("---")
    if st.button("Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_bar = ""
        st.rerun()

# --- Initialize Local Chat History & Input Buffers ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render Existing Chat Thread ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 🛠️ Interactive Math Input Helper Toolbar ---
st.write("### 🛠️ Math Input Helper")
st.markdown("📋 **Quick-Copy Symbols:** Highlight and copy these characters to paste into your input bar below:  \n`^` (Power) | `√` (Square Root) | `π` (Pi) | `θ` (Theta) | `×` (Multiply) | `÷` (Divide) | `∫` (Integral) | `Δ` (Delta)")

# Horizontal layout for quick-launch question templates
st.markdown("**Quick-Load Problem Starters:**")
col1, col2, col3 = st.columns(3)
if col1.button("📐 Exponent Problem", use_container_width=True):
    st.session_state.chat_bar = "How do I simplify an expression with a power like x^3 * x^2?"
if col2.button("🔍 Root Radical", use_container_width=True):
    st.session_state.chat_bar = "Can you guide me through solving a radical problem like √32?"
if col3.button("📈 Derivative Concept", use_container_width=True):
    st.session_state.chat_bar = "I need help finding the derivative of a function."

st.write("---")

# --- Socratic Prompt Engine ---
SYSTEM_INSTRUCTION = (
    "You are 'BC TigerMath AI', a strict Socratic mathematics tutor and the premier BC Math Specialist. "
    "CRITICAL DIRECTIVE: NEVER give the user the final solution or write out a complete step-by-step answer upfront, "
    "even if they explicitly ask you to 'just give me the answer'. Your core job is to guide them to discover it.\n\n"
    "Follow these instructional rules:\n"
    "1. When given a math problem, identify the next mathematical step internally, but only provide ONE small hint or ask ONE target question to guide the student to that step. Make sure to provide the hint so the user can understand what to do. \n"
    "2. If the user says they are completely stuck, provide a brief micro-explanation of the underlying rule (like the chain rule, power rule, or factoring rules) or give a simple parallel example. Then, ask them to apply it back to their original problem.\n"
    "3. Keep responses highly interactive and conversational. Never write long blocks of text; keep messages to a few sentences max.\n"
    "4. If they make an error, point out the breakdown in logic gently and ask a clarifying question to help them self-correct.\n"
    "5. Only confirm the final answer after they have calculated it themselves."
)

# --- Handle New User Interaction ---
# Connecting the key="chat_bar" lets our toolbar programmatically update the field text instantly
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
