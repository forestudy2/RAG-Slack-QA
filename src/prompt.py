from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def summary_prompt(query, relevant_docs):
    """

    질문에 대한 프롬프트를 생성하는 함수.
    """
    prompt = f"""
    당신은 찾고자 하는 관련 문서를 찾아주고 내용을 반환해주는 AI 에이전트입니다.

    텍스트에서 다음과 같은 마크업 기호 및 불필요한 기호를 모두 제거해주세요. 더불어 문장을 보기 쉽게 구성하세요:
    - **굵은 글씨 표시**: 예를 들어 **이런 기호**
    - ## 제목 표시 기호
    - 기타 불필요한 기호

    다음 질문에 답하십시오: '{query}'.
    아래 문서들 중에서 질문과 관련된 문서의 경로와 요약을 반환해 주세요.
    관련 문서들 중에서 질문과 가장 관련이 있는 문서들에 대해서만 답변해 주세요.
    문장이 길어지면 문장을 넘겨 보기 쉽게 구분해주세요.

    관련 문서 정보:
    {', '.join(relevant_docs)}
    """
    return prompt


def resume_prompt(query, relevant_docs):
    """
    이력서 관련 질문에 대한 프롬프트를 생성하고 AI 에이전트가 질문에 답하도록 설정합니다.
    """

    document_info_str = "\n".join(
        [f"내용: {doc.page_content}" for doc in relevant_docs]
    )

    prompt = f"""
    당신은 "김수현"의 이력서에 대한 정보를 전달하는 AI 에이전트입니다.
    이력서에 관한 다음 질문이 들어오면 관련된 답을 상세하게 답해주세요. 

    텍스트에서 다음과 같은 마크업 기호 및 불필요한 기호를 모두 제거해주세요. 더불어 문장을 보기 쉽게 구성하세요: 
    - **굵은 글씨 표시**: 예를 들어 **이런 기호**
    - ## 제목 표시 기호
    - 기타 불필요한 기호

    당신은 철자와 문법을 정확하게 수정하여 텍스트를 깔끔하게 만듭니다.
    당신은 문장 구조를 개선하여 읽기 쉽고 전문적인 글로 변환합니다.
    당신은 각 문장에 적절한 이모지를 추가하여 콘텐츠를 더욱 흥미롭게 만듭니다.
    당신은 텍스트의 표현력을 높여 글쓰기 품질을 향상시킵니다.
    문장이 길어지면 문장을 넘겨 보기 쉽게 구분해주세요.

    다음 질문에 답하십시오: {query}

    관련 문서 내용: {document_info_str}
    """
    return prompt


def conversation_prompt():
    """
    대화 프롬프트 템플릿을 생성합니다.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "당신은 사용자와 대화를 나누고 감정을 공유하는 AI 에이전트입니다. "
                "사용자의 감정을 이해하고 이해한 내용을 토대로 대화를 주도해주시고 조언도 해주세요.\n\n"
                "텍스트에서 다음과 같은 마크업 기호 및 불필요한 기호를 모두 제거해주세요. 더불어 문장을 보기 쉽게 구성하세요:\n"
                "- **굵은 글씨 표시**: 예를 들어 **이런 기호**\n"
                "- ## 제목 표시 기호\n"
                "- 기타 불필요한 기호\n\n"
                "당신은 각 문장에 적절한 이모지를 추가하여 표정 지어주세요.\n"
                "문장이 길어지면 문장을 넘겨 보기 쉽게 구분해주세요.",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "입력: {question}"),
        ]
    )


def search_prompt(current_datetime, question, formatted_docs):
    """질문과 문서 내용을 기반으로 프롬프트 템플릿을 생성합니다."""
    return ChatPromptTemplate.from_template(
        "현재 시간과 날짜({current_datetime})를 반영하여, 대한민국 기준으로 다음 질문에 대한 상세한 답변을 해주세요.\n"
        "질문: {question}\n"
        "제공된 정보는 다음과 같습니다. 반드시 한국어로 답변해주세요. : {formatted_docs}"
    ).format(
        current_datetime=current_datetime,
        question=question,
        formatted_docs=formatted_docs,
    )
