import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable

from load_prompts import load_prompt
# from Retrievers.ensembleRetriever import ensemble_retriever
from Retrievers.contextRetriever import context_retriever
from Retrievers.contextRetriever import course_context_retriever

from dotenv import load_dotenv
load_dotenv()

#---------------------------------#
#-------- Deploy Settings --------#
#---------------------------------#
from google.oauth2 import service_account
import google.generativeai as genai  # genai import 추가

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
)

# Gemini 구성
genai.configure(
    credentials=credentials,
)
###################################


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids):
    if session_ids not in st.session_state["store_main"]:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state["store_main"][session_ids] = ChatMessageHistory()
    return st.session_state["store_main"][session_ids]  # 해당 세션 ID에 대한 세션 기록 반환

@traceable
def create_chain() :
    # prompt
    prompt = load_prompt("prompts/basic.yaml")
    prompt.messages.insert(1, MessagesPlaceholder(variable_name="chat_history"))

    # model - 인증정보 추가
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        credentials=credentials
    )

    # output parser
    output_parser = StrOutputParser()

    # chain
    chain = (
        {
            "context": lambda x: context_retriever().invoke(x["question"]),
            "question": lambda x: x["question"] if isinstance(x, dict) else x,
            "chat_history": lambda x: x["chat_history"]
        }
        | prompt
        | llm
        | output_parser
    )
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    return chain_with_history 

def create_course_chain(start_page, end_page):
    # prompt
    prompt = load_prompt("prompts/basic.yaml")
    prompt.messages.insert(1, MessagesPlaceholder(variable_name="chat_history"))

    # model - 인증정보 추가
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        credentials=credentials
    )

    # output parser
    output_parser = StrOutputParser()

    # retriever
    retriever = course_context_retriever(start_page=start_page, end_page=end_page)

    # chain
    chain = (
        {
            "context": lambda x: retriever.invoke(x["question"]),
            "question": lambda x: x["question"] if isinstance(x, dict) else x,
            "chat_history": lambda x: x["chat_history"]
        }
        | prompt
        | llm
        | output_parser
    )
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    return chain_with_history 