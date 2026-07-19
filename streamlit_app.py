import streamlit as st

from utils.pdf_reader import read_pdf
from utils.chunking import create_chunks
from utils.embedding import create_embeddings
from utils.retrieval import build_index
from utils.rag_pipeline import generate_answer
from utils.memory import add_message, get_history_text

# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="AI PDF Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* Main container */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#F8FAFC;
}

/* Chat messages */
div[data-testid="stChatMessage"]{
    border-radius:12px;
    padding:12px;
}

/* Metric cards */
div[data-testid="metric-container"]{
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:10px;
}

/* Hide Streamlit footer */
footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# Title
# --------------------------------

st.markdown("""
# 🤖 AI PDF Research Assistant
### Chat with your PDF using Retrieval-Augmented Generation (RAG)
""")

st.markdown(
    "Upload a PDF, process it, and ask intelligent questions with **page-aware citations**."
)

st.divider()


# --------------------------------
# Session State
# --------------------------------

default_states = {

    "index": None,
    "chunks": None,
    "processed": False,
    "current_file": None,
    "messages": [],
    "pages": 0

}


for key, value in default_states.items():

    if key not in st.session_state:
        st.session_state[key] = value



# --------------------------------
# Sidebar
# --------------------------------

with st.sidebar:

    st.markdown("## 📂 Document")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"],
        help="Upload a PDF document to start chatting."
    )

    st.divider()

    st.markdown("## 📊 Document Statistics")

    if st.session_state.processed:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Pages",
                st.session_state.pages
            )

        with col2:
            st.metric(
                "Chunks",
                len(st.session_state.chunks)
            )

    else:

        st.info(
            "No document processed."
        )

    st.divider()

    st.markdown("## 🤖 AI Stack")

    st.markdown("""
**Embedding Model**

`all-MiniLM-L6-v2`

**Vector Database**

`FAISS`

**LLM**

`Gemini Flash`

**Architecture**

`Retrieval-Augmented Generation`
""")

    st.divider()

    if st.button(
        "🧹 Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    with st.expander("ℹ️ About Project"):

        st.write("""
This project demonstrates a complete
Retrieval-Augmented Generation (RAG)
pipeline using:

- PyMuPDF
- LangChain Text Splitter
- Sentence Transformers
- FAISS
- Gemini API
- Streamlit
""")



# --------------------------------
# Process PDF Button
# --------------------------------

if uploaded_file is not None:


    if st.session_state.current_file != uploaded_file.name:

        st.session_state.current_file = uploaded_file.name

        st.session_state.processed = False

        st.session_state.index = None

        st.session_state.chunks = None

        st.session_state.messages = []



    if st.button(
        "🚀 Process Document"
    ):


        with st.status(
            "Processing PDF...",
            expanded=True
        ):


            st.write(
                "📖 Extracting pages..."
            )

            pages = read_pdf(
                uploaded_file
            )


            st.write(
                "✂️ Creating chunks..."
            )

            chunks = create_chunks(
    pages,
    source=uploaded_file.name
)


            st.write(
                "🧠 Generating embeddings..."
            )

            embeddings = create_embeddings(
                chunks
            )


            st.write(
                "🔍 Building FAISS index..."
            )

            index = build_index(
                embeddings
            )


            st.session_state.index = index

            st.session_state.chunks = chunks

            st.session_state.pages = len(pages)

            st.session_state.processed = True


            st.write(
                "✅ Document ready!"
            )


        st.success(
            "PDF processed successfully!"
        )

# --------------------------------
# Welcome Screen
# --------------------------------

if uploaded_file is None:

    st.info("👋 Welcome to AI PDF Research Assistant")

    st.markdown("""
### 📖 Chat with your PDF using AI

Upload a PDF document and ask questions in natural language.

---

### 🚀 How it works

1. 📂 Upload a PDF
2. 🚀 Click **Process Document**
3. 💬 Ask questions
4. 📚 Receive answers with page references

---

### ✨ Features

- Semantic Chunking
- Sentence Transformer Embeddings
- FAISS Vector Search
- Gemini AI
- Page-aware References

---

⬅️ Start by uploading a PDF from the sidebar.
""")

    st.stop()



# --------------------------------
# Chat History
# --------------------------------

for message in st.session_state.messages:


    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )



# --------------------------------
# Chat Input
# --------------------------------

question = st.chat_input(
    "Ask something about your PDF..."
)



if question:


    if not st.session_state.processed:

        st.warning(
            "Please process the PDF first."
        )

        st.stop()



    # User message

    st.session_state.messages = add_message(
    st.session_state.messages,
    "user",
    question
)


    with st.chat_message(
        "user"
    ):

        st.write(
            question
        )



# --------------------------------
# Generate Answer
# --------------------------------

if question:

    with st.chat_message("assistant"):

        with st.spinner("Searching your document..."):

            history = get_history_text(
                st.session_state.messages
            )


            answer, sources, context = generate_answer(
                question,
                st.session_state.index,
                st.session_state.chunks,
                history
            )


        # AI Answer

        st.markdown("### 🤖 AI Assistant")

        st.write(
            answer
        )


        # Source Pages

        if sources:

            st.markdown("---")

            st.markdown(
                "#### 📚 Source Pages"
            )


            cols = st.columns(
                min(len(sources), 4)
            )


            for i, source in enumerate(sources):

                with cols[i % len(cols)]:

                    st.info(
                        f"📄 {source['source']}\n\n"
                        f"Page {source['page']}"
                    )


        # Retrieved Context

        with st.expander(
            "🔍 View Retrieved Context"
        ):

            st.code(
                context,
                language="text"
            )


    # --------------------------------
    # Save Assistant Message
    # --------------------------------

    st.session_state.messages = add_message(
        st.session_state.messages,
        "assistant",
        answer
    )


    st.divider()



st.caption(
    "🚀 Python + Machine Learning Mini Project | Built with PyMuPDF • Sentence Transformers • FAISS • Gemini • Streamlit"
)