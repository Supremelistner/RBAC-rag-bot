# frontend/app.py
import streamlit as st
import requests
import os

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(page_title="RBAC RAG Chatbot", page_icon="🤖")

st.title("RBAC RAG Chatbot — (Peter Pandey)")

if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# --- Authentication UI ---
with st.sidebar:
    st.header("Login / Signup")
    auth_tab = st.radio("", ["Login", "Signup"])

    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")
    role = st.selectbox("Role (for signup)", ["Employee", "Finance", "Marketing", "HR", "Engineering", "C_Level"], key="role_input")

    if auth_tab == "Signup":
        if st.button("Create Account"):
            payload = {"username": username, "password": password, "role": role}
            r = requests.post(f"{API_BASE}/auth/signup", json=payload)
            if r.ok:
                st.success("Account created. Please login.")
            else:
                st.error(r.json().get("detail") or r.text)
    else:
        if st.button("Login"):
            payload = {"username": username, "password": password}
            r = requests.post(f"{API_BASE}/auth/login", json=payload)
            if r.ok:
                data = r.json()
                st.session_state.token = data.get("access_token") or data.get("access_token") or data.get("token") or data.get("accessToken")
                st.session_state.role = data.get("role")
                st.session_state.username = username
                st.success(f"Logged in as {username} ({st.session_state.role})")
            else:
                st.error(r.json().get("detail") or r.text)

# --- Chat UI ---
st.markdown("---")
if not st.session_state.token:
    st.info("Please login from the sidebar to start chatting.")
    st.stop()

st.subheader("Ask a question")
question = st.text_area("Your question", height=120, key="question_input")
if st.button("Send"):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    r = requests.post(f"{API_BASE}/rag/query", json={"question": question}, headers=headers)
    if r.status_code == 200:
        resp = r.json()
        st.markdown(f"**Answer ({resp.get('role')}):**")
        st.write(resp.get("answer"))
        st.markdown("**Sources:**")
        for s in resp.get("sources", []):
            st.markdown(f"- **{s.get('source')}** (role: {s.get('role')})")
            st.code(s.get("content_snippet"))
    else:
        st.error(r.text)
