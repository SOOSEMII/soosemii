# __import__('pysqlite3')
# import sys
# import pysqlite3
# sys.modules['sqlite3'] = sys.modules["pysqlite3"]

import streamlit as st
from langchain_core.messages.chat import ChatMessage
from default_chain import create_chain
from dotenv import load_dotenv
from langchain_teddynote import logging

load_dotenv()
logging.langsmith("SOOSEMII")


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


#---------------------------------#
#---------- UI Settings ----------#
#---------------------------------#
st.title("🧽수세미✨")

# sidebar
with st.sidebar :
    # clear dialouge
    clear_btn = st.button("♻️대화 초기화")
    catalog_btn = st.link_button("✅수강편람 다운로드", "https://board.sejong.ac.kr/boardview.do?pkid=166710&currentPage=2&searchField=ALL&siteGubun=19&menuGubun=1&bbsConfigFK=335&searchLowItem=ALL&searchValue=")
    session_id = st.text_input("세션 ID를 입력하세요.", "abc123")
    st.write("대화 기억을 위한 입력입니다. 아무 숫자나 입력하셔도 됩니다.")
    st.markdown('[Powered by SMARCLE](https://www.smarcle.dev/)', unsafe_allow_html=True)

description = st.container(border=True)
description.write("""
                 안녕하세요🤗 수세미입니다🧽\n
                 수강편람에서 어떤 지점이 궁금하신가요? 제가 답해드릴게요.\n
                 최대한 구체적으로 작성해주시면 제가 더 잘 도와드릴 수 있어요.\n
                 1️⃣정확한 확인을 위해 꼭 **📖수강편람** 을 함께 확인해주세요.\n
                 2️⃣수강편람과 수강신청 공지는 좌측 사이드바의 **[✅수강편람 다운로드]** 를 눌러보세요.\n
                 3️⃣사용방법은 좌측 사이드바의 **[사용방법]** 을 확인해주세요.\n
                 ⚠️수강편람에 적혀있지 않은 내용은 답변이 어려워요😥
                 """)

#---------------------------------#
#-------- Message Storing --------#
#---------------------------------#
# dialouge storage
if "messages_main" not in st.session_state :
    st.session_state["messages_main"] = []
    
if "store_main" not in st.session_state:
    st.session_state["store_main"] = {}

# add new message to storage
def add_message(role, message, avatar) :
    st.session_state["messages_main"].append(ChatMessage(role=role, content=message, avatar=avatar))

# print all dialouge
def print_messages() :
    for chat_message in st.session_state["messages_main"] :
        if chat_message.role == "user":
            avatar = "🧑‍💻"  # 사용자 아바타
        elif chat_message.role == "assistant":
            avatar = "🧽"  # AI 아바타
        else:
            avatar = None  # 다른 역할의 경우 기본 아바타 사용
        st.chat_message(chat_message.role, avatar=avatar).write(chat_message.content)


#---------------------------------#
#---------- User Action ----------#
#---------------------------------#
if clear_btn:
    st.session_state["messages_main"] = []

# show previous dialouge
print_messages()

# user input
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# error window
warning_msg = st.empty()

if "chain_main" not in st.session_state:
    st.session_state["chain_main"] = create_chain()
    
# if input
if user_input :
    # temporary
    chain = st.session_state["chain_main"]
    if chain is not None :
        response = chain.stream(
            # 질문 입력
            {"question": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        # user input
        st.chat_message("user", avatar="🧑‍💻").write(user_input)

        with st.chat_message("assistant", avatar="🧽"):
            # create empty container and print token by stream
            container = st.empty()
            ai_answer = ""
            for token in response :
                ai_answer += token
                container.markdown(ai_answer)

            # add dialougue to storage
            add_message("user", user_input, avatar="🧑‍💻")
            add_message("assistant", ai_answer, avatar="🧽")
    else :
        warning_msg.error("문제가 발생했습니다.")
