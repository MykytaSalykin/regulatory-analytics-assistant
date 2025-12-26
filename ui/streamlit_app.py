import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Regulatory Analytics Assistant", page_icon="📊", layout="wide"
)

st.title("📊 Regulatory Analytics Assistant")
st.markdown("*AI-powered banking regulatory and risk analysis*")

st.markdown("---")

with st.container():
    query = st.text_area(
        "Enter your question:",
        placeholder="e.g., What are the main drivers of profitability expectations?",
        height=100,
    )

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)

    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()

if ask_button and query.strip():
    with st.spinner("Processing your query..."):
        try:
            response = requests.post(
                f"{API_URL}/query", json={"query": query}, timeout=30
            )

            if response.status_code == 200:
                data = response.json()

                st.markdown("---")

                query_type = data.get("query_type", "unknown")

                if query_type == "analytics":
                    badge_color = "blue"
                    badge_text = "📊 Analytics"
                elif query_type == "document":
                    badge_color = "green"
                    badge_text = "📄 Document"
                else:
                    badge_color = "orange"
                    badge_text = "🔄 Hybrid"

                st.markdown(f"**Query Type:** :{badge_color}[{badge_text}]")

                st.markdown("### Answer")
                st.markdown(data.get("answer", "No answer provided"))

                sources = data.get("sources", [])
                if sources:
                    st.markdown("---")
                    st.markdown("### 📚 Sources")

                    for i, src in enumerate(sources, 1):
                        file_name = src.get("file", "Unknown")
                        page = src.get("page")
                        score = src.get("score")

                        source_text = f"**{i}.** {file_name}"
                        if page:
                            source_text += f" (page {page})"
                        if score:
                            source_text += f" — relevance: {score:.2%}"

                        st.markdown(source_text)

            elif response.status_code == 400:
                st.error("❌ Invalid query. Please enter a valid question.")

            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Cannot connect to the API. Make sure the FastAPI server is running."
            )

        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")

        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")

elif ask_button:
    st.warning("⚠️ Please enter a question first.")

st.markdown("---")

with st.expander("ℹ️ About this tool"):
    st.markdown("""
    This is a **Proof of Concept** for a Regulatory Analytics Assistant.
    
    **Capabilities:**
    - **Analytics queries**: Statistical analysis of EBA survey data
    - **Document queries**: RAG-based retrieval from regulatory PDFs
    - **Hybrid queries**: Combined analytics + document context
    
    **Data sources:**
    - EBA Transparency Exercise 2025 RAQ statistical annex
    - EBA Risk Assessment Report (2025)
    - RAQ Booklet (Autumn 2025)
    """)

with st.expander("💡 Example queries"):
    st.markdown("""
    **Analytics queries:**
    - "What are the main drivers of profitability expectations?"
    - "Show me the distribution of responses for profitability"
    
    **Document queries:**
    - "What does the EBA Risk Assessment Report say about credit risk?"
    - "According to EBA guidelines, what are the key risk indicators?"
    
    **Hybrid queries:**
    - "How many banks expect profitability to increase and what does EBA say about it?"
    """)
