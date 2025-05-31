from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma

def lecture_retriever() : 
    persist_db = Chroma(
        persist_directory="./lecs",
        embedding_function=UpstageEmbeddings(model="embedding-passage"),
        collection_name="lectures",
    )
    retriever = persist_db.as_retriever()
    return retriever

def search_lecture(user_input) :
    persist_db = Chroma(
        persist_directory="./lecs",
        embedding_function=UpstageEmbeddings(model="embedding-passage"),
        collection_name="lectures",
    )
    return persist_db.similarity_search(user_input, k=1)