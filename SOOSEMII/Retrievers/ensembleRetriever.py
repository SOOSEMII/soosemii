import json
from langchain.schema import Document
from langchain.retrievers import  EnsembleRetriever
from Retrievers.bm25Retriever import bm25_retriever
from Retrievers.summaryRetriever import summary_retriever

def ensemble_retriever() : 
    retriever = EnsembleRetriever(
        retrievers=[bm25_retriever(), summary_retriever()],
        weights=[0.5, 0.5],
    )
    return retriever

def search_ensemble(user_input) :
    retriever = ensemble_retriever()
    return retriever.get_relevant_documents(user_input)

def course_ensemble(start_page=None, end_page=None):
    # BM25 Retriever
    bm25 = bm25_retriever()
    
    # Summary (MultiVectorRetriever)
    summary = summary_retriever()
    
    if start_page is not None and end_page is not None:
        # MultiVectorRetriever의 vectorstore에 필터 적용
        summary.vectorstore.search_kwargs = {
            "filter": {"page": {"$gte": start_page, "$lte": end_page}}
        }
        
        # BM25 필터링을 위한 새로운 메서드 추가
        def get_relevant_documents(query):
            docs = bm25.get_relevant_documents(query)
            return [
                doc for doc in docs 
                if start_page <= doc.metadata.get("page", 0) <= end_page
            ]
        bm25.get_relevant_documents = get_relevant_documents
    
    retriever = EnsembleRetriever(
        retrievers=[bm25, summary],
        weights=[0.5, 0.5],
    )
    return retriever
