import streamlit as st
from db import initialize_prompt_and_text
from llm import generate_responses
from openai import OpenAI
import dotenv

dotenv.load_dotenv()


### Sidebar
st.sidebar.title("Inputs")
st.sidebar.write('modify these then press Start/Restart on the right')
lead_first_name = st.sidebar.text_input("Lead First Name", value = "Susan")
lead_last_name = st.sidebar.text_input("Lead Last Name", value = "Smith")
lead_email = st.sidebar.text_input("Lead Email", value = "susan@gmail.com")
company_name = st.sidebar.text_input("Company Name", value = "Acme Co")
company_description = st.sidebar.text_area("Company Description", value = "Acme Co is proud to be the third largest bricks provider in Southeast Nebraska. We create a variety of bricks. Red bricks, blue bricks, even green bricks. We have small bricks and large bricks. If you need decent bricks for your construction project, call us today.")
booking_link = st.sidebar.text_input("Booking Link", value = "www.calendly.com/chicory/30-min-meeting")
temp = 0#st.sidebar.slider("Temperature", min_value = 0.0, max_value = 1.0, value = 0.0, step = 0.1)
model = "gpt-4-turbo"#st.sidebar.selectbox("Model", ["gpt-4-1106-preview", "gpt-3.5-turbo"])
max_tokens = 200#st.sidebar.slider("Max Tokens", min_value = 50, max_value = 500, value = 200, step = 50)
####Main Bar
    

client = OpenAI()

st.title("Chicory: Cole Testing Site")

if st.button("Start/Restart"):
    #clear all session state
    st.session_state.clear()
    st.session_state.messages = []
    st.session_state.lead_first_name = lead_first_name
    st.session_state.lead_last_name = lead_last_name
    st.session_state.lead_email = lead_email
    st.session_state.company_name = company_name
    st.session_state.company_description = company_description
    st.session_state.booking_link = booking_link
    st.session_state.temp = temp
    st.session_state.model = model
    st.session_state.max_tokens = max_tokens
    st.rerun()

if "messages" in st.session_state:

    #Initialize system prompt and initial text
    if st.session_state.get('system_prompt') is None and st.session_state.get('initial_text') is None:
        initialize_prompt_and_text(st.session_state)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-1106-preview"

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            generate_responses(st.session_state)
            
        #     messages=[
        #             {"role": m["role"], "content": m["content"]}
        #             for m in st.session_state.messages
        #         ]
        #     messages.insert(0, {"role": "system", "content": st.session_state["system_prompt"]})

        #     stream = client.chat.completions.create(
        #         model=st.session_state["openai_model"],
        #         messages = messages,
        #         temperature = 0,

        #     )

        #     response = st.write_stream(stream)
        # st.session_state.messages.append({"role": "assistant", "content": response})












