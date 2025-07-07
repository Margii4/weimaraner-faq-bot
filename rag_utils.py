import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def load_faq_docs_docx(filepath):
    loader = Docx2txtLoader(filepath)
    docs = loader.load()
    return docs

def split_docs(docs, chunk_size=500, chunk_overlap=80):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)

def build_vector_store(docs):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    PineconeVectorStore.from_documents(
        docs,
        embeddings,
        index_name=os.getenv("PINECONE_INDEX"),
        pinecone_api_key=os.getenv("PINECONE_API_KEY"),
    )
    return True

def get_vector_store():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    vectorstore = PineconeVectorStore(
        index_name=os.getenv("PINECONE_INDEX"),
        embedding=embeddings,
        pinecone_api_key=os.getenv("PINECONE_API_KEY"),
    )
    return vectorstore
