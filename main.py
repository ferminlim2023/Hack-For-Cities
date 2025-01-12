# https://www.gettingstarted.ai
# email: jeff@gettingstarted.ai
# written by jeff

# thanks jeff - broke & broken bois
# Codebase is built off the initial hackaton demo

# Import required modules from the LangChain package
import streamlit as st
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
import requests
from preprocessing import *
from prompts import *
import os
import json

def generate(prompt,model_id,max_output=4000,temp=0,top_k=1,repeat_penalty=1.1,stream=True):
    url = "http://127.0.0.1:11434/api/generate"
    params = {
        "temperature": temp,
        "repeat_penalty":repeat_penalty,
        "top_p":1,
        "top_k":top_k,
        "num_predict":max_output,
        "stop":["[/INST]","<|user|>","<|endoftext|>","<|assistant|>","<eof>"]
    }

    body = {
        "model":model_id,
        "options":params,
        "stream":stream,
        "prompt":prompt
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        # "Authorization": f"Bearer {self.access_token}" # No need for authorization as it is locally hosted using Ollama
    }

    response = requests.post(
        url,
        headers=headers,
        json=body,
        stream=True
    )


    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    yield ""
    # Stream the response
    for line in response.iter_lines():
        if line:  # Ensure the line is not empty
            decoded_line = line.decode("utf-8").strip()
            
            # Check if the line starts with "data: "
            if decoded_line.startswith("data: "):
                json_data = decoded_line[len("data: "):]  # Remove the "data: " prefix
            else:
                json_data = decoded_line
            try:
                # Attempt to load the JSON data
                data = json.loads(json_data)
                generated_text = data.get("response", "")

                yield generated_text.replace("$","\$")
                if data.get("done"):
                    st.session_state['tokens']['prompt_tokens'] = data.get("prompt_eval_count")
                    st.session_state['tokens']['response_tokens'] = data.get("eval_count")
                    st.session_state['tokens']['total_tokens'] = data.get("prompt_eval_count") + data.get("eval_count")
                    print("Checking session state tokens",st.session_state['tokens'])

            except json.JSONDecodeError:
                print("Failed to decode JSON:", json_data)
            except Exception as e:
                print("An error occurred:", e)

    yield ""

# checking if collection exist, if no, create new collection
from preprocessing import embeddings_model
vectorstore = Chroma(persist_directory="./recordb", embedding_function=embeddings_model)
#print(vectorstore._collection.count())

if vectorstore._collection.count()==0:
    all_docs = os.listdir("./newdocs")
    vectorstore = vectorstore_ingest(all_docs)

img_url = "https://www.hdb.gov.sg/html/Dashboard/Foundation/Theming/images/site-logo-small.png"

st.title(":house: ChatBTO")
st.sidebar.image(img_url)
st.sidebar.title("Parameter Selection")
model_id = "granite3.1-dense:8b"

st.chat_message("assistant").markdown("Hey its ChatBTO! Here to help you with all your HDB questions!")

temp = 0
top_k = 30
max_token = 4000
repeat_penalty = 1
enable_stream = True

# Clears all messages
reset = st.sidebar.button("Reset",type="primary")
if reset:
    st.session_state.messages = []
    

if "tokens" not in st.session_state: 
    st.session_state['tokens'] = {
    "prompt_tokens":0,
    "response_tokens":0,
    "total_tokens":0
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"].replace("$","\$"))

if prompt := st.chat_input("Ask me about anything HDB BTO related..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt.replace("$","\$"))

    with st.chat_message("assistant"):
        context = vectorstore.similarity_search(prompt, k=5)
        print(context)
        qna_prompt = question_prompt(context, prompt, st.session_state.messages[:-1])
        stream = generate(qna_prompt,model_id,max_token,temp,top_k,repeat_penalty,enable_stream)
        response = st.write_stream(stream)

    st.sidebar.write("Prompt Tokens Used: ",st.session_state['tokens']['prompt_tokens'])
    st.sidebar.write("Response Tokens Used: ",st.session_state['tokens']['response_tokens'])
    st.sidebar.write("Total Tokens Used: ",st.session_state['tokens']['total_tokens'])

    st.session_state.messages.append({"role": "assistant", "content": response})