import streamlit as st
from transformers import pipeline

# Initialize Session State
if "users" not in st.session_state:
    st.session_state.users = {}

# Sign Up Function
def signup():
    st.title("Sign Up")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        if username in st.session_state.users:
            st.warning("Username already exists!")
        else:
            st.session_state.users[username] = password
            st.success("User registered! Please log in.")
            st.experimental_rerun()

# Login Function
def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.success("Login successful!")
            st.session_state.logged_in_user = username
            st.experimental_rerun()
        else:
            st.error("Invalid credentials!")

# Dashboard Function
def dashboard(username):
    st.title(f"Welcome, {username}!")
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose a mode", ["AI Chatbot", "Notes Generator"])

    if app_mode == "AI Chatbot":
        st.subheader("Chat with AI")
        user_input = st.text_input("Enter your message:", key="chat_input")
        if st.button("Send"):
            chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")
            response = chatbot(user_input)
            st.write(f"AI: {response[0]['generated_text']}")
    
    elif app_mode == "Notes Generator":
        st.subheader("Generate Notes")
        topic = st.text_input("Enter the topic:", key="notes_topic")
        if st.button("Generate"):
            summarizer = pipeline("summarization")
            notes = summarizer(topic, max_length=100, min_length=30, do_sample=False)
            st.write(notes[0]['summary_text'])

# Main App Logic
if "logged_in_user" not in st.session_state:
    page = st.sidebar.selectbox("Select a Page", ["Login", "Sign Up"])
    if page == "Sign Up":
        signup()
    elif page == "Login":
        login()
else:
    dashboard(st.session_state.logged_in_user)
