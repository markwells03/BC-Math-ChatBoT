import streamlit as st
from groq import Groq

# Page Styling - Customized for Benedict College
st.set_page_config(page_title="BC TigerMath AI", page_icon="🐅", layout="centered")
st.title("🐅 BC TigerMath AI")
st.caption("Your Campus BC Math Specialist | Powered by Groq (Free Tier)")

# --- Sidebar: Secure API Key Input ---
with st.sidebar:
    st.header("Configuration")
    groq_key = st.text_input("Enter Groq API Key:", type="password", help="Grab yours for free at console.groq.com")
    st.markdown("[Get a free Groq API Key](https://console.groq.com/)")
    
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
    
    if not groq_key:
        st.error("Please provide your Groq API Key in the sidebar to send messages!")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # Format message history for Groq's SDK
    formatted_messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for msg in st.session_state.messages:
        formatted_messages.append({"role": msg["role"], "content": msg["content"]})
        
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Initialize official Groq client
            client = Groq(api_key=groq_key)
            
            # Using Llama 3.3 70B for strong mathematical reasoning
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
            st.error(f"An unexpected error occurred: {e}")