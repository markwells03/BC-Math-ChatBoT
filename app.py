import streamlit as st
from groq import Groq

# Page Styling - Customized for Benedict College
st.set_page_config(page_title="BC TigerMath AI", page_icon="🐅", layout="centered")
st.title("🐅 BC TigerMath AI")
st.caption("Your Campus BC Math Specialist | Powered by Groq (Free Tier)")

# --- Sidebar: Cleaned Up Layout ---
with st.sidebar:
    st.header("Control Panel")
    st.info("The BC Math Specialist is fully authenticated and ready to assist!")
    
    st.write("---")
    if st.button("Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Initialize Local Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render Existing Chat Thread ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Socratic Prompt Engine ---
SYSTEM_INSTRUCTION = (
    "You are 'BC TigerMath AI', a strict Socratic mathematics tutor and the premier BC Math Specialist. "
    "CRITICAL DIRECTIVE: NEVER give the user the final solution or write out a complete step-by-step answer upfront, "
    "even if they explicitly ask you to 'just give me the answer'. Your core job is to guide them to discover it.\n\n"
    "Follow these instructional rules:\n"
    "1. When given a math problem, identify the next mathematical step internally, but only provide ONE small hint or ask ONE target question to guide the student to that step.\n"
    "2. If the user says they are completely stuck, provide a brief micro-explanation of the underlying rule (like the chain rule, power rule, or factoring rules) or give a simple parallel example. Then, ask them to apply it back to their original problem.\n"
    "3. Keep responses highly interactive and conversational. Never write long blocks of text; keep messages to a few sentences max.\n"
    "4. If they make an error, point out the breakdown in logic gently and ask a clarifying question to help them self-correct.\n"
    "5. Only confirm the final answer after they have calculated it themselves."
)

# --- Handle New User Interaction ---
if user_query := st.chat_input("Ask a question..."):
    
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
            # Fetches from your Streamlit Cloud Secrets management dashboard automatically
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
            st.error(f"Authentication Error: The backend secret key is missing or improperly formatted.")
            st.info("Technical details: " + str(e))
