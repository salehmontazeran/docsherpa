import streamlit as st
from dotenv import load_dotenv

from src.retreive.chat_engine import chat_engine_v1

if __name__ == "__main__":
    load_dotenv()

    if "chat_engine" not in st.session_state.keys():
        st.session_state.chat_engine = chat_engine_v1

    st.set_page_config(
        page_title="Chat with Docs Sherpa",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    st.title("Docs Sherpa")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Type anything!"}]

    if prompt := st.chat_input("Your input"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner(""):
                response = st.session_state.chat_engine(query_text=prompt or "")
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
