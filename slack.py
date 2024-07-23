import os
import torch
import dotenv
from slack_bolt import App
from operator import itemgetter
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_teddynote import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# 새로운 ChatPromptTemplate 정의
prompt = PromptTemplate.from_template(
    """당신은 질문 응답 챗봇이며 간단한 대화도 가능합니다. 사용자가 질문을 하면 그에 맞는 답변을  제공합니다.
    질문에 대한 답변은 사용자의 질문과 관련이 있어야 합니다. 불필요한 추가 질문이나 신뢰도에 대한 내용은 텍스트는 포함하지 마세요.
    항상 한국어(Korean)로 대답해주세요. 응답은 최대 100자 이내로 간결하게 작성해주세요.
    그 외의 관련 없는 대화거나 질문에 대한 답변이 불가능하다면 답변할 수 없다고 자세한 질문 부탁드린다고 답변해주세요.

#Previous Chat History:
{chat_history}

#Question: 
{question} 

#Answer:"""
)

# llm 생성
llm = ChatOllama(model="EEVE-Korean-10.8B:latest", max_tokens=100, temperature=0)

# 세션 기록을 저장할 딕셔너리
store = {}

# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_id):
    print(f"[대화 세션ID]: {session_id}")
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 일반 Chain 생성
chain = (
    {
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history"),
    }
    | prompt
    | llm
    | StrOutputParser()
)


# RunnableWithMessageHistory 생성
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,                               # 세션 기록을 가져오는 함수
    input_messages_key="question",                     # 사용자의 질문이 템플릿 변수에 들어갈 key
    history_messages_key="chat_history",               # 기록 메시지의 키
)

# 슬랙 앱 초기화
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Slack 이벤트 핸들러
@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    session_id = body['event']['channel']
    message = body['event']['text']

    # chain_with_history를 사용하여 응답 생성
    response = chain_with_history.invoke(
        {"question": message},
        config={"configurable": {"session_id": session_id}}
    )
    say(response)

# Slack 메시지 핸들러
@app.message(".*")
def message_handler(message, say, logger):
    session_id = message['channel']
    text = message['text']

    # chain_with_history를 사용하여 응답 생성
    response = chain_with_history.invoke(
        {"question": text},
        config={"configurable": {"session_id": session_id}}
    )
    say(response)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()