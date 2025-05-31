from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma

embeddings = UpstageEmbeddings(model="embedding-passage")

def context_retriever() : 
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory="2025-1-0217",
        collection_name="2025-1-0217"
    )
    retriever = vectorstore.as_retriever(kwargs={"k":5})
    return retriever

def search_context(user_input) :
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory="2025-1-0217",
        collection_name="2025-1-0217"
    )
    answer = vectorstore.similarity_search(user_input, k=5)
    return answer


def course_context_retriever(start_page=None, end_page=None):
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory="2025-1-0217",
        collection_name="2025-1-0217"
    )

    # Define a filter dictionary for Chroma using $and operator
    filter_dict = {}
    if start_page is not None and end_page is not None:
        filter_dict = {
            "$and": [
                {"page": {"$gte": start_page}},
                {"page": {"$lte": end_page}}
            ]
        }
    elif start_page is not None:
        filter_dict = {"page": {"$gte": start_page}}
    elif end_page is not None:
        filter_dict = {"page": {"$lte": end_page}}

    # Return a retriever with the filter applied
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5, "filter": filter_dict})
    return retriever
