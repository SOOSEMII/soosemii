import pickle
from langchain.schema import Document
from langchain.retrievers import BM25Retriever

FILE_PATH = "data/2025_md.pkl"

def load_documents(file_path):
    with open(file_path, 'rb', encoding='utf-8') as f:
        documents = pickle.load(f)

documents = load_documents(FILE_PATH)

def custom_preprocess(query):
    if isinstance(query, dict):
        return query.get("question", "").split()
    return query.split()

def bm25_retriever() : 
    retriever = BM25Retriever.from_documents(
        documents,
        k=20,
        preprocess_func=custom_preprocess,
    )
    return retriever