import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="Accounting AI Auditor", layout="wide")

st.title("📑 Accounting AI Auditor")
st.markdown("""
This AI agent uses **LangGraph**, **LangChain**, and **RAG** to help you audit invoices and financial reports.
It can query a SQL database for structured data and search through documents using hybrid retrieval.
""")

# Sidebar for file uploads
with st.sidebar:
    st.header("Upload Documents")
    uploaded_file = st.file_uploader("Upload an invoice or report (PDF/MD)", type=["pdf", "md"])
    if uploaded_file:
        if st.button("Process Document"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            try:
                response = requests.post("http://localhost:8000/upload", files=files)
                if response.status_code == 200:
                    st.success("File uploaded successfully! Processing in background.")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about invoices, vendors, or the audit report..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Agent is thinking and checking data..."):
                response = requests.post(
                    "http://localhost:8000/query",
                    json={"query": prompt, "thread_id": "streamlit_user"}
                )
                if response.status_code == 200:
                    answer = response.json()["response"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Error from backend.")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")

# Show Mock Data Info
with st.expander("System Info & Mock Data"):
    st.write("The system is pre-loaded with mock invoices and a 2024 Audit Report.")
    csv_path = "accounting_rag_app/data/invoice_summary.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.dataframe(df)
