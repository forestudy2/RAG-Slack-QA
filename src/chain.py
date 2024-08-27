# 내일 할 일은 감정형 대화 멀티턴 구현! & 검색 엔진 구현 & API 만드는 것 조사
# 끝나면 slack 연동 혹은 웹 페이지 연동

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from prompt import summary_prompt, resume_prompt, conversation_prompt
from retriever import load_summary_retriever, load_resume_retriever


def summary_chain(query):
    """
    사용자의 쿼리에 대해 검색을 수행하고, 관련된 문서 요약과 함께 질문에 대한 답변을 반환하는 함수.
    """
    summary_retriever = load_summary_retriever()

    # 검색 수행
    relevant_docs = summary_retriever.invoke(query)

    if not relevant_docs:
        return "검색된 문서가 없습니다."

    # 검색된 문서에서 PDF 경로와 요약을 추출
    document_info = []
    for doc in relevant_docs:
        pdf_path = doc.metadata["pdf"]
        summary = doc.page_content  # 문서의 요약 내용
        document_info.append(f"문서 경로: {pdf_path}\n요약: {summary}")

    # 질문 프롬프트 생성
    prompt = summary_prompt(query, document_info)

    # 질문 체인 실행
    summary_chain = (
        ChatOpenAI(model_name="gpt-4o-mini", temperature=0) | StrOutputParser()
    )

    response = summary_chain.invoke(prompt)
    return response


def resume_chain(query):
    """
    이력서 관련 질문에 대해 리트리버와 AI 체인을 이용해 답변을 생성하는 함수.
    """

    resume_retriever = load_resume_retriever()

    relevant_docs = resume_retriever.invoke(query)

    if not relevant_docs:
        return "검색된 문서가 없습니다."

    # 프롬프트 생성
    prompt = resume_prompt(query, relevant_docs)

    # 질문 체인 실행
    resume_chain = (
        ChatOpenAI(model_name="gpt-4o-mini", temperature=0) | StrOutputParser()
    )
    response = resume_chain.invoke(prompt)

    return response


# 세션 기록을 저장할 딕셔너리
store = {}


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_id):
    if session_id not in store:  # 세션 ID가 store에 없는 경우
        store[session_id] = ChatMessageHistory()
    return store[session_id]  # 해당 세션 ID에 대한 세션 기록 반환


def conversation_chain(query, session_id="default_session"):
    """
    사용자의 쿼리에 대해 감정을 이해하고 답변을 반환하는 함수.
    """

    # 세션 기록 가져오기
    chat_history = get_session_history(session_id)

    # 프롬프트 생성
    prompt_template = conversation_prompt()
    prompt = prompt_template.format_messages(
        question=query, chat_history=chat_history.messages  # chat_history를 전달
    )

    # LLM 생성
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    # 체인 생성
    chain = prompt_template | llm | StrOutputParser()

    # 대화 기록을 포함한 체인 생성
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,  # 세션 기록을 가져오는 함수
        input_messages_key="question",  # 사용자의 질문이 템플릿 변수에 들어갈 key
        history_messages_key="chat_history",  # 기록 메시지의 키
    )

    # 질문 체인 실행
    response = chain_with_history.invoke(
        {"question": query},
        config={"configurable": {"session_id": session_id}},
    )

    return response
