import json
from lectureRetriever import search_lecture
from contextRetriever import search_context
from ensembleRetriever import ensemble_retriever
from memory import get_history

# 사용자 질문 + 강의 정보
def add_stuInfo(user_input, stuInfo) :
    prompt = "질문: {user_input}\n학생 정보:\n{stuInfo}\n"
    return prompt

def rag_history(user_input, SessionState) :
    result = get_history(user_input, SessionState)

    # 반환된 결과에서 강의명만 추출
    content = result[0]

    # 사용자 질문과 강의명 결합
    combined_query = user_input + content
    answer = ensemble_retriever()
    return answer 