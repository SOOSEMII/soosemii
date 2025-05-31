import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_history(user_input, SessionState):
    # 메시지가 없는 경우 빈 리스트 반환
    if len(SessionState) <= 3:
        return ["none"]
    
    # 저장된 메시지에서 content만 추출
    stored_messages = [
        {"role": msg.role, "content": msg.content} 
        for msg in SessionState
    ]
    messages_content = [msg["content"] for msg in stored_messages]
    
    # 현재 입력과 저장된 메시지를 합쳐서 벡터화
    all_texts = messages_content + [user_input]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # 코사인 유사도 계산
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    
    # 상위 k개의 유사한 메시지 찾기
    k = 3
    top_indices = similarity_scores.argsort()[-(k):][::-1]
    similar_messages = [stored_messages[i] for i in top_indices]

    # chain에 전달할 대화 기록 생성
    chat_history = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in similar_messages
    ])
    
    return chat_history