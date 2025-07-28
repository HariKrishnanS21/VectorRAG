import streamlit as st
import requests

st.set_page_config(page_title="Airport Chatbot",layout="wide")
st.title("AirBot")
st.markdown("Ask me anything about Changi or jewel airport")

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

with st.container():
    user_query=st.text_input("Your Question",placeholder="type your questions here...")
    col1,col2=st.columns([1,1])
    with col1:
        send_clicked = st.button("Send")
    with col2:
        clear_clicked = st.button("Clear Chat")

if clear_clicked:
    st.session_state.chat_history = []
    st.rerun()

if send_clicked and user_query.strip():
    with st.spinner("Thinking..."):
        try:
            api_url = "https://vectorrag.onrender.com/query"
            response = requests.post(api_url, json={"question": user_query})

            if response.status_code == 200:
                answer = response.json()["answer"]
                st.session_state.chat_history.append(("You", user_query))
                st.session_state.chat_history.append(("Bot", answer))
            else:
                st.error("API returned an error. Please try again.")

        except Exception as e:
            st.error(f"Failed to reach the backend: {e}")

for sender, message in st.session_state.chat_history:
    with st.chat_message(name="user" if sender == "You" else "assistant"):
        st.markdown(f"**{sender}:** {message}")
