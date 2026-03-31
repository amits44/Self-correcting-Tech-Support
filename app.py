import streamlit as st
from graph import app
from dotenv import load_dotenv
load_dotenv()

st.title("Self-Correcting Tech Support")
query = st.text_input("Describe your issue...")

if st.button("Ask") and query:
    with st.spinner("Agent thinking..."):
        result = app.invoke({"question": query, "retry_count": 0})
    st.markdown("### Answer")
    st.write(result["generation"])
    with st.expander("Sources used"):
        for doc in result["documents"]:
            st.write(doc.page_content[:300] + "...")