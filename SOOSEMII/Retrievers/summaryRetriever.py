from langchain_chroma import Chroma
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import LocalFileStore
from langchain_upstage import UpstageEmbeddings

VECTOR_DB_PATH = "./MultiVectorSummary/multiVectorDB"
DOCS_DB_PATH = "./MultiVectorSummary/docsDB"

def summary_retriever() :
    # 요약 정보를 저장할 벡터 저장소를 생성합니다.
    summary_vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        collection_name="summaries",
        embedding_function=UpstageEmbeddings(model="embedding-passage"),
    )

    # 부모 문서를 저장할 저장소를 생성합니다.
    docstore = LocalFileStore(DOCS_DB_PATH)

    # 문서 ID를 저장할 키 이름을 지정합니다.
    id_key = "doc_id"

    # 검색기를 초기화합니다. (시작 시 비어 있음)
    summary_retriever = MultiVectorRetriever(
        vectorstore=summary_vectorstore,  # 벡터 저장소
        byte_store=docstore,  # 바이트 저장소
        id_key=id_key,  # 문서 ID 키
    )
    
    return summary_retriever

def course_summary_retriever(start_page=None, end_page=None):
    # 요약 정보를 저장할 벡터 저장소를 생성합니다.
    summary_vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        collection_name="summaries",
        embedding_function=UpstageEmbeddings(model="embedding-passage"),
    )

    # 부모 문서를 저장할 저장소를 생성합니다.
    docstore = LocalFileStore(DOCS_DB_PATH)

    # 문서 ID를 저장할 키 이름을 지정합니다.
    id_key = "doc_id"

    # 페이지 필터 정의
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

    # MultiVectorRetriever 초기화
    summary_retriever = MultiVectorRetriever(
        vectorstore=summary_vectorstore,
        docstore=docstore,
        id_key=id_key,
        search_kwargs={"filter": filter_dict}
    )
    
    return summary_retriever
