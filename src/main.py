import streamlit as st


@st.cache_resource(show_spinner=False)
def get_index():

    # chat mock. return input in reverse.
    def chat(message):
        return message[::-1]

    return chat


index = get_index()
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index

st.set_page_config(
    page_title="Chat with Docs Sherpa",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Mirorrer")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Type anything, I mirror it."}]

if prompt := st.chat_input("Your input"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner(""):
            response = st.session_state.chat_engine(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
