from openai import OpenAI
import streamlit as st

st.title("Chatbot")
temp=st.slider('Temperature',min_value=0.0,max_value=1.0,step=0.1)

client = OpenAI(api_key=st.secrets["GROQ_API_KEY"],
                base_url="https://api.groq.com/openai/v1")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "llama-3.3-70b-versatile"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=temp,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})