import streamlit as st
from groq import Groq

# ====================== LOAD CONTACTS ======================
@st.cache_data
def load_contacts():
    try:
        with open("contacts.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return content.strip()
    except FileNotFoundError:
        st.error("benedict_info.txt file not found!")
        return "Contact information not available."

CONTACTS_INFO = load_contacts()

# ====================== PAGE SETUP ======================
st.set_page_config(page_title="BC TigerMath AI", page_icon="🐅", layout="centered")

# Custom CSS (your original styling)
st.markdown("""
    <style>
    h1 { color: #FFD700 !important; font-family: 'Arial Black', Gadget, sans-serif; }
    .stCaption { color: #F0F2F6 !important; font-style: italic; }
    div.stButton > button {
        background-color: #4C145E !important;
        color: #FFD700 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 8px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #FFD700 !important;
        color: #4C145E !important;
        border: 2px solid #4C145E !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🐅 BC TigerMath AI")
st.caption("Your Campus BC Math Specialist | Created by Mark Wells and Jamazio Mcphee")

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Control Panel")
    st.info("The BC Math Specialist is fully authenticated and ready to assist!")
    st.write("---")
    if st.button("Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ====================== SYSTEM INSTRUCTION ======================
SYSTEM_INSTRUCTION = f"""
You are 'BC TigerMath AI', a strict Socratic mathematics tutor and the premier BC Math Specialist at Benedict College.

**CAMPUS CONTACT INFORMATION** (Use this when asked):
{CONTACTS_INFO}

🔴 CAMPUS KNOWLEDGE EXCEPTION:
- If the user asks about contact information, Financial Aid, Admissions, Campus Police, President’s Office, or any department contacts, 
  answer **directly and clearly** using the information above. Do not use Socratic method for contact questions.
- For general Benedict College questions (history, colors, sports, etc.), answer warmly and directly.

📐 MATHEMATICS DIRECTIVES:
- For all math problems, NEVER give the final answer directly. Use Socratic questioning.
- Give one small hint or ask one guiding question at a time.
- Keep responses concise and conversational.
"""

# ====================== CHAT HISTORY ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ====================== MATH TOOLBAR ======================
st.write("### 🛠️ Math Input Helper")
st.markdown("**Quick-Copy Symbols:** `^` `√` `π` `θ` `×` `÷` `∫` `Δ`")

col1, col2, col3, col4 = st.columns(4)
if col1.button("📐 Exponent Problem", use_container_width=True):
    st.session_state.chat_bar = "How do I simplify x^3 * x^2?"
if col2.button("🔍 Root Radical", use_container_width=True):
    st.session_state.chat_bar = "Can you guide me through √32?"
if col3.button("📈 Derivative", use_container_width=True):
    st.session_state.chat_bar = "Help me find the derivative of a function."
if col4.button("🐾 BC History", use_container_width=True):
    st.session_state.chat_bar = "When was Benedict College founded?"

st.write("---")

# ====================== CHAT INPUT ======================
if user_query := st.chat_input("Ask a question...", key="chat_bar"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Prepare messages for Groq
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
                temperature=0.7,
                stream=True
            )

            for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error("Error connecting to AI. Please try again.")
            st.info(f"Details: {str(e)}")
