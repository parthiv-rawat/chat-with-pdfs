import streamlit as st
import os
from utils.pdf_index import create_or_load_index, save_uploaded_pdfs
# from dotenv import load_dotenv

openai.api_key = st.secrets["OPENAI_API_KEY"]
# load_dotenv()

st.set_page_config(page_title="Chat with your PDFs", layout="centered")
st.title("📄 Chat with Your PDFs")

upload_folder = "pdfs"
os.makedirs(upload_folder, exist_ok=True)

# Initialize session history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def clean_response(text):
    ignore_keywords = ["context:", "source:", "metadata:"]
    lines = text.strip().split("\n")
    return "\n".join(
        line for line in lines
        if not any(line.lower().startswith(k) for k in ignore_keywords) and line.strip()
    )

# Step 1: Upload PDFs
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    new_files_uploaded = save_uploaded_pdfs(uploaded_files, upload_folder)

    if new_files_uploaded:
        with st.spinner("Indexing your PDFs..."):
            index = create_or_load_index(upload_folder, force_recreate=True)
        st.success("New PDFs indexed successfully!")
    else:
        index = create_or_load_index(upload_folder)
        st.info("No new files found. Loaded existing index.")

    st.success(f"Uploaded {len(uploaded_files)} file(s):")
    for file in uploaded_files:
        st.write(f"- {file.name}")

    # Step 2: Ask Questions
    query = st.text_input("💬 Ask something from your PDFs:")

    if query:
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        cleaned = clean_response(str(response))

        # Save to chat history
        st.session_state.chat_history.append({"question": query, "response": cleaned})

        st.markdown("### 🤖 Answer")
        st.write(cleaned)

    # Step 3: Show chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📜 Chat History")
        for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
            st.markdown(f"**Q{i}:** {chat['question']}")
            st.markdown(f"**A{i}:** {chat['response']}")

else:
    st.info("Upload PDFs to start chatting.")
