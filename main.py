# https://www.gettingstarted.ai
# email: jeff@gettingstarted.ai
# written by jeff

# Don't forget to set your OPEN_AI_KEY
# In your terminal execute this command: export OPENAI_API_KEY="YOUR_KEY_HERE"

# Import required modules from the LangChain package
import streamlit as st
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
# from langchain_ollama import ChatOllama
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.embeddings import OllamaEmbeddings

# from docling.document_converter import DocumentConverter

# Create a vector store with a sample text
# from langchain_core.vectorstores import InMemoryVectorStore

from preprocessing import *
from prompts import *
from watsonx import *

import os

wx = WatsonxAI()

# model = "granite3.1-dense:8b"

# Load a PDF document and split it into sections
# loader = PyPDFLoader("./docs/Application Form for Enhanced CPF Housing Grant.pdf")
# docs = loader.load_and_split()

# load pdf into docling and parse it
# def load_pdf(f):
#     source = f"docs/{f}"
#     converter = DocumentConverter()
#     docs = converter.convert(source).document.export_to_markdown()
#     return docs

# Initialize the Ollama chat model
# llm = ChatOllama(
#     model=model
# )

# Initialize the Ollama embeddings
# embed = OllamaEmbeddings(
#     model=model
# )

# checking if collection exist, if no, create new collection
from preprocessing import embeddings_model
vectorstore = Chroma(persist_directory="./recordb", embedding_function=embeddings_model)

print(vectorstore._collection.count())
# print(vectorstore.get())

if vectorstore._collection.count()==0:
    all_docs = os.listdir("./docs")
    vectorstore = vectorstore_ingest(all_docs)

img_url = "https://www.hdb.gov.sg/html/Dashboard/Foundation/Theming/images/site-logo-small.png"

st.title(":house: ChatBTO")
st.sidebar.image(img_url)
st.sidebar.title("Parameter Selection")
model_id = "OLLAMA_GRANITE_3_1_8B_CODE_INSTRUCT" #st.sidebar.selectbox("Please select a model",("OLLAMA_GRANITE_3_1_8B_CODE_INSTRUCT"))

st.chat_message("assistant").markdown("Hey its ChatBTO! Here to help you with all your HDB questions!")

# col_1,col_2 = st.sidebar.columns(2)

# with col_1:
#     temp = 0#st.slider("Temperature (0-1)",0.0,1.0,0.0,0.1)
#     top_k = 0#st.slider("Top K",0,100,1,1)
# with col_2:
#     max_token = st.slider("Max Number of Tokens",0,10000,4000,100)
#     repeat_penalty = st.slider("Repeat Penalty", 0.0,2.0,1.1,0.1)
# enable_stream = st.sidebar.toggle("Enable Word Stream")

temp = 0
top_k = 0
max_token = st.sidebar.slider("Max Number of Tokens",0,10000,4000,100)
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
        context = vectorstore.similarity_search(prompt, k=3)
        print(context)
        qna_prompt = question_prompt(context, prompt)
        # print(qna_prompt)
        if (getattr(wx,model_id,None)==None):
            st.warning("Please select model")
            st.stop()
        stream = wx.watsonx_gen_stream(qna_prompt,getattr(wx,model_id,""),max_token,temp,top_k,repeat_penalty,enable_stream)
        response = st.write_stream(stream)

    st.sidebar.write("Prompt Tokens Used: ",st.session_state['tokens']['prompt_tokens'])
    st.sidebar.write("Response Tokens Used: ",st.session_state['tokens']['response_tokens'])
    st.sidebar.write("Total Tokens Used: ",st.session_state['tokens']['total_tokens'])

    st.session_state.messages.append({"role": "assistant", "content": response})