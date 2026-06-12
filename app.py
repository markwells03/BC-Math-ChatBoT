import streamlit as st
from groq import Groq
from docx import Document

# =====================================
# PAGE SETUP
# =====================================

st.set_page_config(
    page_title="BC TigerMath AI",
    page_icon="🐅",
    layout="centered"
)

# =====================================
# CUSTOM STYLE
# =====================================

st.markdown("""
<style>

h1{
color:#FFD700!important;
font-family:'Arial Black',sans-serif;
}

.stCaption{
color:#F0F2F6!important;
font-style:italic;
}

div.stButton > button{
background:#4C145E!important;
color:#FFD700!important;
border:2px solid #FFD700!important;
border-radius:8px;
font-weight:bold;
}

div.stButton > button:hover{
background:#FFD700!important;
color:#4C145E!important;
}

div[data-testid="stSidebar"]{
background:#1A1A1A;
}

div[data-testid="stChatInput"]{
border:2px solid #4C145E!important;
border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "chat_bar" not in st.session_state:
    st.session_state.chat_bar=""

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.header("Control Panel")
    
    st.info("The BC Math Specialist is fully authenticated and ready to assist!")
    st.write("---")

    # 1. Initialize session state for language if it doesn't exist
    if "language" not in st.session_state:
        st.session_state.language = "English"

    # 2. Use the session state variable to control the radio
    st.radio(
    "🌍 Choose Language",
    ["English", "Español", "Français"],
    key="language"
    )

    previous_language = st.session_state.get(
    "previous_language",
    st.session_state.language
    )

if previous_language != st.session_state.language:
    st.session_state.messages = []
    st.session_state.previous_language = st.session_state.language
    st.rerun()


    st.write("---")

    if st.button("Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_bar = ""
        st.rerun()
# =====================================
# LANGUAGE SUPPORT
# =====================================

captions = {

    "English":
    "Your Campus BC Math Specialist",

    "Español":
    "Tu Especialista Matemático BC",

    "Français":
    "Votre spécialiste mathématique BC"

}

LANGUAGE_PROMPT = {

    "English":
    "You MUST respond ONLY in English.",

    "Español":
    "Debes responder ÚNICAMENTE en español.",

    "Français":
    "Vous devez répondre UNIQUEMENT en français."

}

# =====================================
# TITLE
# =====================================

st.title("🐅 BC TigerMath AI")

st.caption(
    captions[st.session_state.language]
)

# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_INSTRUCTION = f"""

You are BC TigerMath AI.

{LANGUAGE_PROMPT[st.session_state.language]}

You are:

1. A Socratic Mathematics Tutor

2. A Benedict College Information Assistant

BENEDICT RULES:

If asked about Benedict College:

Answer directly.

Do NOT use Socratic teaching.

Only use verified Benedict records.

If unavailable say:

'I don't see that in my Benedict records.'

MATH RULES:

Start with:

Rule Used:
Formula:
Why It Applies:

Then provide ONE hint.

Keep answers short.

Never reveal full solutions.

Only confirm after the student solves.

If stuck:
Give a tiny explanation.

"""
```

# =====================================
# INPUT
# =====================================

if user_query:=st.chat_input(
"Ask a question...",
key="chat_bar"
):

    st.session_state.messages.append({

        "role":"user",

        "content":
        user_query

    })

    context=""

    keywords=[

        "benedict",
        "admissions",
        "housing",
        "registrar",
        "financial aid",
        "president",
        "email",
        "phone",
        "contact"

    ]

    if any(

        word
        in
        user_query.lower()

        for word
        in
        keywords

    ):

        context=(
            search_benedict(
                user_query
            )
        )

    final_prompt=(
        SYSTEM_INSTRUCTION
    )

    if context:

        final_prompt+=(

            "\n\n"

            +

            context

        )


    formatted_messages = [
        {
            "role": "system",
            "content": final_prompt
        }
    ]

    for msg in st.session_state.messages:
    formatted_messages.append({
        "role": msg["role"],
        "content": msg["content"]
    })

    with st.chat_message(
        "assistant"
    ):
        placeholder=(
            st.empty()
        )

        answer=""

        try:

            client=Groq(

                api_key=

                st.secrets[
                    "GROQ_API_KEY"
                ]

            )

            stream=(
                client
                .chat
                .completions
                .create(

                    model=
                    "llama-3.3-70b-versatile",

                    messages=
                    formatted_messages,

                    temperature=
                    0.6,

                    stream=True

                )
            )

            for chunk in stream:

                delta=(
                    chunk
                    .choices[0]
                    .delta
                    .content
                )

                if delta:

                    answer+=delta

                    placeholder.markdown(
                        answer
                        +
                        "▌"
                    )

            placeholder.markdown(
                answer
            )

            st.session_state.messages.append({

                "role":
                "assistant",

                "content":
                answer

            })

        except Exception as e:

            st.error(
                "API Error"
            )

            st.code(
                str(e)
            )
```
