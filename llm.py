from openai import OpenAI
import streamlit as st
import os
import re
import random
from icecream import ic

openai = OpenAI(max_retries = 5)



def generate_streaming_response(self, messages, model = 'gpt-4-turbo-preview', max_tokens=200):
    try:
        response = openai.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens, stream=True, temperature = 0)
        big_chunk = ""
        for chunk in response:
            chunk = chunk.choices[0].delta.content
            if chunk:
                big_chunk += chunk
                if chunk in ['!', '.', '?']:
                    to_yield = big_chunk
                    big_chunk = ""
                    yield to_yield

    
    except Exception as e:
        error_message = f"Attempt failed: {e}"
        print(error_message)



#generate openai response; returns messages with openai response
def generate_responses(session_state):
  messages = session_state.messages

  system_prompt = session_state.system_prompt
  system_prompt = {"role": "system", "content": system_prompt}

  key = os.environ.get("OPENAI_API_KEY")
  openai.api_key = key

  response = openai.chat.completions.create(model=session_state.model, messages=[system_prompt , *messages], max_tokens=session_state.max_tokens, temperature = session_state.temp)
  response = response.choices[0].message.content
  session_state.messages.append({"role": "assistant", "content": response})
  st.rerun()
  # 

  # split_response = split_sms(response)
  # ic(split_response)
  # for section in split_response:
  #   section = {
  #     "role": "assistant", 
  #     "content": section
  #   }
  #   messages.append(section)
  #   session_state.messages = messages[1:]
  # st.rerun()


