from docling.document_converter import DocumentConverter
from langchain_ollama import OllamaEmbeddings
import chromadb.utils.embedding_functions as embedding_functions
from preprocessing import *
from prompts import *
import streamlit as st
import os

embeddings = OllamaEmbeddings(model="llama3.2")

vectorstore = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

# checking if collection exist, if no, create new collection
# vectorstore = Chroma(persist_directory="./recordb", embedding_function=embeddings_model)

if vectorstore._collection.count()==0:
    all_docs = os.listdir("./docs")
    for doc in all_docs:
        vectorstore = vectorstore_ingest(f"{doc}")

# source = "https://arxiv.org/pdf/2408.09869"  # document per local path or URL
source = r"docs/Guide To Apply For HDB BTO.pdf"
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())  # output: "## Docling Technical Report[...]"

print(f"{os.getcwd()}/docs")
# print(os.listdir(f"{os.getcwd()}/docs"))