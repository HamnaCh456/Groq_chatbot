

import asyncio
import streamlit as st
from groq import AsyncGroq
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
st.markdown(""" <style>
    body {
        background-color: grey;
        color: white;
    }
    .stApp {
        background-color: grey;
    }
    </style>
            """,unsafe_allow_html=True)
async def main(prompt:str,chat_history:dict,personality:str,ai_model:str):
    client = AsyncGroq(api_key=api_key)

    chat_completion = await client.chat.completions.create(
        #
        # Required parameters
        #
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
                "role": "system",
                "content": "You are a helpful {personality}.Dont answer anything which is not related to your field."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": f"This is the chat history:{chat_history} and current prompt is: {prompt}",
            }
        ],

        # The language model which will generate the completion.
        model=ai_model,

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become
        # deterministic and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 2048 tokens shared between prompt and completion.
      

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    # Print the completion returned by the LLM.
    print("new output")
    print(chat_completion.choices[0].message.content)
    result=chat_completion.choices[0].message.content
    return result




if "chat_history" not in st.session_state:
    st.session_state.chat_history={"prompts_history":[],"response_history":[]}
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input=""
if "ai_model_input" not in st.session_state:
    st.session_state.ai_model_input=""
if "personality_input" not in st.session_state:
    st.session_state.personality_input=""

def submit_callback():
    result=asyncio.run(main(prompt,st.session_state.chat_history,st.session_state.personality_input,st.session_state.ai_model_input))
    st.session_state.chat_history["response_history"].append(result)
    st.write(result)
col1,col2=st.columns([0.8,0.2],vertical_alignment="bottom",border=False)

print("Enter the prompt:")
with col1:
    ai_model=st.radio("Select the model:",["llama-3.3-70b-versatile","llama-3.1-8b-instant"],key="ai_model_input")
    personality=st.radio("Select the personality:",["Maths_teacher","Doctor","Travel Guide","Chef","Tech Support"],key="personality_input")
    prompt=st.text_input("Enter the prompt",key="prompt_input")


#prompt=input()
    st.session_state.chat_history["prompts_history"].append(prompt)
with col2:
    st.button("",icon =":material/send:",key="2",on_click=submit_callback)