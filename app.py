```python
# --------------------------
# BENEDICT FILE SUPPORT
# --------------------------

from docx import Document


def load_benedict_doc(path="benedict_info.docx"):

    try:
        doc = Document(path)

        text = []

        for p in doc.paragraphs:
            line = p.text.strip()

            if line:
                text.append(line)

        return "\n".join(text)

    except Exception:
        return ""


BENEDICT_DATA = load_benedict_doc()


def get_benedict_context(query):

    query = query.lower()

    sections = BENEDICT_DATA.split("\n\n")

    matches = []

    for section in sections:

        if query in section.lower():

            matches.append(section)

        else:

            score = 0

            for word in query.split():

                if word in section.lower():
                    score += 1

            if score >= 2:
                matches.append(section)

    return "\n\n".join(matches[:3])


# --------------------------
# CHAT INPUT
# --------------------------

if user_query := st.chat_input(
    "Ask a question...",
    key="chat_bar"
):

    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    # --------------------------
    # BUILD SYSTEM MESSAGE
    # --------------------------

    system_message = SYSTEM_INSTRUCTION

    benedict_words = [
        "benedict",
        "admissions",
        "financial aid",
        "campus police",
        "phone",
        "email",
        "contact",
        "housing",
        "registrar",
        "president",
        "department"
    ]

    if any(
        word in user_query.lower()
        for word in benedict_words
    ):

        records = get_benedict_context(user_query)

        if records:

            system_message += f"""

VERIFIED BENEDICT INFORMATION

{records}

IMPORTANT:
Use ONLY information shown above.

Never guess.
Never invent phone numbers.
Never estimate emails.

If information is unavailable:
say:

'I could not find that in the Benedict records.'
"""

    formatted_messages = [
        {
            "role": "system",
            "content": system_message
        }
    ]

    for msg in st.session_state.messages:

        formatted_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # --------------------------
    # SEND TO GROQ
    # --------------------------

    with st.chat_message("assistant"):

        placeholder = st.empty()

        answer = ""

        try:

            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            stream = (
                client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=formatted_messages,
                    temperature=0.3,
                    stream=True
                )
            )

            for chunk in stream:

                text = (
                    chunk
                    .choices[0]
                    .delta
                    .content
                )

                if text:

                    answer += text

                    placeholder.markdown(
                        answer + "▌"
                    )

            placeholder.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            st.error(str(e))
```
