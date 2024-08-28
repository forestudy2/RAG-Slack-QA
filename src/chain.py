import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_community.chat_message_histories import ChatMessageHistory
from prompt import summary_prompt, resume_prompt, conversation_prompt, search_prompt
from retriever import load_summary_retriever, load_resume_retriever

load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)


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
    summary_chain = llm | StrOutputParser()

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
    resume_chain = llm | StrOutputParser()
    response = resume_chain.invoke(prompt)

    return response


# 세션 기록을 저장할 딕셔너리
store = {}


# 세션 ID를 기반으로 세션  기록을 가져오는 함수
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
    # llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

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


# 통합된 search_chain 함수
def search_chain(query):
    retriever = TavilySearchAPIRetriever(k=3, search_depth="advanced")

    # 현재 시간과 날짜를 얻기
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 검색한 문서 결과를 얻는다
        documents = retriever.invoke(query)

        # 검색한 문서 결과가 없거나 빈 경우 처리
        if not documents:
            return "검색 결과가 없습니다. 올바른 검색어를 다시 입력해주세요."

        # 검색한 문서 내용을 하나의 문단으로 합친다
        formatted_docs = "\n\n".join(doc.page_content for doc in documents)

        # 프롬프트 템플릿을 생성한다
        prompt = search_prompt(current_datetime, query, formatted_docs)

        # 체인을 구성한다
        chain = (
            RunnablePassthrough.assign(context=(lambda x: x["input"]) | retriever)
            | RunnableLambda(
                lambda _: formatted_docs
            )  # 여기서 formatted_docs를 직접 사용
            | RunnableLambda(lambda _: prompt)  # 여기서 prompt를 직접 사용
            | llm
            | StrOutputParser()
        )

        # 질문에 대한 답변을 생성한다
        response = chain.invoke(
            {
                "input": query,
                "current_datetime": current_datetime,
                "question": query,
                "formatted_docs": formatted_docs,
            }
        )

        # 체인 결과가 비어 있는 경우를 처리
        if not response:
            return "결과가 없습니다. 다시 시도해 주세요."

        return response

    except requests.exceptions.HTTPError as http_err:
        # 400 Bad Request와 같은 HTTP 오류를 처리
        if http_err.response.status_code == 400:
            return "검색 결과가 없습니다. 올바른 검색어를 다시 입력해주세요."
        else:
            return f"HTTP 오류가 발생했습니다: {http_err}. 다시 시도해 주세요."

    except Exception as e:
        # 일반적인 예외 처리
        return f"예기치 않은 오류가 발생했습니다: {str(e)}"
