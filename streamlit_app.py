import streamlit as st
import requests
import base64

# --- CONFIGURATION ---
API_ANALYZE_ENDPOINT = "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/analyze/analyze"
API_REVIEW_ENDPOINT = "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/review/update"

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Content Approval System", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""

""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["User Dashboard", "Admin Dashboard"])

# --- USER DASHBOARD ---
if page == "User Dashboard":
    st.title("📄 User Dashboard")
    st.markdown("Upload your document for automated classification and summarization.")

    uploaded_file = st.file_uploader("Choose a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        file_bytes = uploaded_file.read()
        encoded_file = base64.b64encode(file_bytes).decode("utf-8")

        if st.button("🔍 Analyze Document"):
            with st.spinner("Analyzing with AI..."):
                try:
                    response = requests.post(
                        API_ANALYZE_ENDPOINT,
                        json={"filename": uploaded_file.name, "filedata": encoded_file},
                        headers={"Content-Type": "application/json"}
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.markdown("---")
                        st.subheader("🧠 AI Analysis Result")
                        st.markdown(f"**Classification:** `{result.get('classification', 'N/A')}`")
                        st.markdown(f"**Summary:** {result.get('summary', 'No summary available.')}")
                        if result.get("llm_analysis") == "LLM analysis failed.":
                            st.warning("⚠️ LLM analysis failed. Please check the Lambda logs.")
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")

                except Exception as e:
                    st.error(f"🚨 Exception occurred: {e}")

# --- ADMIN DASHBOARD ---
elif page == "Admin Dashboard":
    st.title("🛡️ Admin Dashboard")
    st.markdown("Review analyzed content and make approval decisions.")

    # Simulated list of documents for review (replace with actual API call or database)
    documents = [
        {"filename": "doc1.pdf", "classification": "Needs Review", "summary": "Summary of doc1"},
        {"filename": "doc2.txt", "classification": "Approved", "summary": "Summary of doc2"},
    ]

    for doc in documents:
        st.markdown("---")
        st.subheader(f"📄 {doc['filename']}")
        st.markdown(f"**Classification:** `{doc['classification']}`")
        st.markdown(f"**Summary:** {doc['summary']}")

        decision = st.radio(f"Decision for {doc['filename']}", ["Approve", "Reject"], key=doc['filename'])
        if st.button(f"Submit Decision for {doc['filename']}"):
            try:
                review_response = requests.post(
                    API_REVIEW_ENDPOINT,
                    json={"filename": doc['filename'], "decision": decision},
                    headers={"Content-Type": "application/json"}
                )
                if review_response.status_code == 200:
                    st.success(f"✅ Decision '{decision}' submitted for {doc['filename']}")
                else:
                    st.error(f"❌ Error submitting decision: {review_response.status_code}")
            except Exception as e:
                st.error(f"🚨 Exception occurred: {e}")