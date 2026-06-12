```python
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

    st.info(
        "The BC Math Specialist is fully authenticated and ready to assist!"
    )

    st.write("---")

    # 🌍 MULTI LANGUAGE BUTTON
    language = st.radio(
        "🌍 Choose Language",
        [
            "English",
            "Español",
            "Français"
        ]
    )

    st.write("---")

    if st.button(
        "Reset Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.chat_bar = ""
        st.rerun()

# =====================================
# LANGUAGE SUPPORT
# =====================================

captions={

"English":
"Your Campus BC Math Specialist",

"Español":
"Tu Especialista Matemático BC",

"Français":
"Votre spécialiste mathématique BC"

}

language_prompt={

"English":
"Respond only in English.",

"Español":
"Respond only in Spanish.",

"Français":
"Respond only in French."

}

# =====================================
# TITLE
# =====================================

st.title("🐅 BC TigerMath AI")

st.caption(
captions[language]
)

# =====================================
# LOAD BENEDICT DOC
# =====================================

def load_benedict_doc():

    try:

        doc=Document(
            "benedict_info.docx"
        )

        lines=[]

        for p in doc.paragraphs:

            text=p.text.strip()

            if text:

                lines.append(
                    text
                )

        return lines

    except:

        return []

BENEDICT_DATA=(
load_benedict_doc()
)

# =====================================
# SEARCH DOC
# =====================================

def search_benedict(
query
):

    query=query.lower()

    results=[]

    for line in BENEDICT_DATA:

        if any(

            word
            in
            line.lower()

            for word
            in
            query.split()

        ):

            results.append(
                line
            )

    return "\n".join(
        results[:20]
    )

# =====================================
# CHAT HISTORY
# =====================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# =====================================
# MATH TOOLBAR
# =====================================

st.write(
"### 🛠️ Math Input Helper"
)

st.markdown("""
`^`
`√`
`π`
`θ`
`×`
`÷`
`∫`
`Δ`
""")

col1,col2,col3=(
st.columns(3)
)

if col1.button(
"📐 Exponent"
):
    st.session_state.chat_bar=(
    "Help simplify x^3*x^2"
)

if col2.button(
"🔍 Radical"
):
    st.session_state.chat_bar=(
    "Help solve √32"
)

if col3.button(
"📈 Derivative"
):
    st.session_state.chat_bar=(
    "Help find derivative"
)

LANGUAGE_PROMPT = {

"English":
"Respond entirely in English.",

"Español":
"Respond entirely in Spanish.",

"Français":
"Respond entirely in French."

}

# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_INSTRUCTION=f"""

You are BC TigerMath AI.

{language_prompt[language]}

You are:

1.
A Socratic Math Tutor

2.
A Benedict College
Information Assistant

BENEDICT RULES:

Answer Benedict
questions directly.

Never use Socratic
teaching for Benedict.

Only use verified
records.

If missing say:

I don't see that
in my Benedict
records.

MATH RULES:

Start with:

Rule Used:

Formula:

Why It Applies:

Then:

Give ONE hint.

Keep answers short.

Never reveal
full solution.

Only confirm
answer after
student solves.

If student
is stuck:

Give a tiny
explanation.

"""

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
"role":"system",

"content":
SYSTEM_INSTRUCTION
+
"\n\n"
+
LANGUAGE_PROMPT[language]

}

]
    formatted_messages.extend(
        st.session_state.messages
    )

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
