import streamlit as st
from groq import Groq
from docx import Document

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="BC TigerMath AI",
    page_icon="🐅",
    layout="centered"
)

# ==========================================
# CUSTOM STYLING
# ==========================================

st.markdown("""
<style>

h1{
color:#FFD700!important;
font-family:'Arial Black';
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

# ==========================================
# HEADER
# ==========================================

st.title("🐅 BC TigerMath AI")
st.caption(
"Your Campus BC Math Specialist | Powered by Groq"
)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Control Panel")

    st.success(
        "BC Math Specialist Ready"
    )

    if st.button(
        "Reset Conversation",
        use_container_width=True
    ):

        st.session_state.messages=[]

        st.rerun()

# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "chat_bar" not in st.session_state:
    st.session_state.chat_bar=""

# ==========================================
# BENEDICT DOC SEARCH
# ==========================================

def load_benedict_doc():

    try:

        doc=Document("benedict_info.docx")

        return [
            p.text.strip()
            for p in doc.paragraphs
            if p.text.strip()
        ]

    except:

        return []

BENEDICT_DATA=load_benedict_doc()

def search_benedict(query):

    matches=[]

    for line in BENEDICT_DATA:

        if any(
            word.lower()
            in line.lower()

            for word in query.split()
        ):

            matches.append(line)

    return "\n".join(matches[:15])

# ==========================================
# LEARNING RESOURCE ENGINE
# ==========================================

def get_learning_resources(text):

    text=text.lower()

    resources={

        "trig":{
            "video":
            "https://www.youtube.com/watch?v=LwCRRUa8yTU",

            "site":
            "https://www.khanacademy.org/math/trigonometry"
        },

        "derivative":{
            "video":
            "https://www.youtube.com/watch?v=ANyVpMS3HL4",

            "site":
            "https://www.khanacademy.org/math/differential-calculus"
        },

        "integral":{
            "video":
            "https://www.youtube.com/@ProfessorLeonard",

            "site":
            "https://www.khanacademy.org/math/integral-calculus"
        },

        "algebra":{
            "video":
            "https://www.youtube.com/@TheOrganicChemistryTutor",

            "site":
            "https://www.khanacademy.org/math/algebra"
        },

        "calculus":{
            "video":
            "https://www.youtube.com/@ProfessorLeonard",

            "site":
            "https://www.khanacademy.org/math/calculus-1"
        }

    }

    for topic in resources:

        if topic in text:

            return resources[topic]

    return None

# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_INSTRUCTION="""

You are BC TigerMath AI.

ROLE 1:
Socratic mathematics tutor.

ROLE 2:
Information assistant for Benedict College.

BENEDICT RULE:
If asked about Benedict College:

Answer directly.

Do not use Socratic teaching.

Only use verified Benedict records.

Never invent data.

If unavailable say:

'I don't see that in my Benedict records.'

MATH RULES:

1.
Show:

Rule Used:

Formula:

Why It Applies:

2.
Give ONE hint.

3.
If stuck:
Explain briefly.

4.
Keep answers short.

5.
Help fix mistakes.

6.
Only confirm answers
after student works.

7.
Never reveal full
solution immediately.

8.
After helping,
recommend:

• One YouTube lesson

• One educational site

Prefer:

Khan Academy

Professor Leonard

Organic Chemistry Tutor

PatrickJMT

"""

# ==========================================
# CHAT HISTORY
# ==========================================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.markdown(
            msg["content"]
        )

# ==========================================
# TOOLBAR
# ==========================================

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

col1,col2,col3=st.columns(3)

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
    "Guide me through √32"
)

if col3.button(
"📈 Derivative"
):
    st.session_state.chat_bar=(
    "Help find derivative"
)

# ==========================================
# USER INPUT
# ==========================================

user_query=st.chat_input(
"Ask a question...",
key="chat_bar"
)

if user_query:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_query
        }
    )

    context=""

    keywords=[

        "benedict",
        "housing",
        "registrar",
        "financial aid",
        "president",
        "email",
        "phone",
        "admissions"

    ]

    if any(
        k in user_query.lower()
        for k in keywords
    ):

        context=search_benedict(
            user_query
        )

    system_message=SYSTEM_INSTRUCTION

    if context:

        system_message+=(
            "\n\nVerified Records:\n"
            +context
        )

    formatted_messages=[

        {
            "role":"system",
            "content":system_message
        }

    ]

    formatted_messages.extend(
        st.session_state.messages
    )

    with st.chat_message(
        "assistant"
    ):

        output=st.empty()

        final=""

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

                    temperature=.6,

                    stream=True

                )
            )

            for chunk in stream:

                text=(
                    chunk
                    .choices[0]
                    .delta.content
                )

                if text:

                    final+=text

                    output.markdown(
                        final+"▌"
                    )

            output.markdown(
                final
            )

            st.session_state.messages.append(
                {
                    "role":
                    "assistant",

                    "content":
                    final
                }
            )

            links=(
                get_learning_resources(
                    user_query
                )
            )

            if links:

                st.write("---")

                st.subheader(
                    "🎥 Continue Learning"
                )

                st.markdown(
                    f"""
▶ [Watch Lesson]
({links['video']})

📚 [Practice]
({links['site']})
"""
                )

        except Exception as e:

            st.error(
                "API Error"
            )

            st.code(
                str(e)
            )
```
