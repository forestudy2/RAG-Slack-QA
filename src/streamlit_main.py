import streamlit as st
import time
from langchain_core.messages import ChatMessage
from chain import summary_chain, resume_chain, conversation_chain, search_chain

# 페이지 설정
st.set_page_config(page_title="MultiMinds", page_icon="🌿")
st.title("MultiMinds 🌿")

# 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = {
        "summary": [],
        "resume": [],
        "conversation": [],
        "search": [],
    }
if "chain" not in st.session_state:
    st.session_state["chain"] = None
if "current_function" not in st.session_state:
    st.session_state["current_function"] = None
if "initial_message_shown" not in st.session_state:
    st.session_state["initial_message_shown"] = False
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""


# 대화 기록 출력
def print_history():
    current_function = st.session_state["current_function"]
    if current_function:
        for msg in st.session_state["messages"][current_function]:
            st.chat_message(msg.role).markdown(msg.content)


# 대화 기록 추가
def add_history(role, content):
    current_function = st.session_state["current_function"]
    if current_function:
        st.session_state["messages"][current_function].append(
            ChatMessage(role=role, content=content)
        )


# 기능에 맞는 체인 설정
def set_chain_for_function(chain_type):
    if chain_type == "문서 검색":
        st.session_state["chain"] = summary_chain
        st.session_state["current_function"] = "summary"
    elif chain_type == "이력서 조회":
        st.session_state["chain"] = resume_chain
        st.session_state["current_function"] = "resume"
    elif chain_type == "감정 기반 대화":
        st.session_state["chain"] = conversation_chain
        st.session_state["current_function"] = "conversation"
    elif chain_type == "실시간 정보 검색":
        st.session_state["chain"] = search_chain
        st.session_state["current_function"] = "search"
    else:
        st.session_state["chain"] = None
        st.session_state["current_function"] = None


# 텍스트를 점진적으로 출력하는 함수
def type_out_text(text, delay=0.03):
    """텍스트를 한 글자씩 점진적으로 출력하며 말풍선으로 표시"""
    display_text = ""
    message_container = st.chat_message("assistant")
    text_container = message_container.markdown("")  # 비어 있는 말풍선 생성

    for char in text:
        display_text += char
        text_container.markdown(display_text)  # 점진적으로 텍스트 추가
        time.sleep(delay)

    return display_text


# 사이드바 설정
with st.sidebar:
    st.write("### 사용할 기능을 선택해 주세요.")

    # 기능 선택 (드롭다운 형식)
    chain_type = st.selectbox(
        "기능 선택",
        [
            "선택하지 않음",
            "문서 검색",
            "이력서 조회",
            "감정 기반 대화",
            "실시간 정보 검색",
        ],
        index=0,
    )

    # 기능 설정
    set_chain_for_function(chain_type)

    # 기능 설명 출력
    function_descriptions = {
        "문서 검색": "📄 **문서 검색**  \n\n문서 내용을 찾기 위한 질문을 입력해주세요.  \n\n질문과 관련된 문서의 경로와 문서에 대한 요약이 출력됩니다.",
        "이력서 조회": "👤 **이력서 조회**  \n\n지원자 '김수현'의 이력서를 보기 위한 질문을 입력해주세요.  \n\n질문과 관련된 자기소개서, 경력사항, 수상 경력, 학력, 프로젝트 등의 내용이 출력됩니다.",
        "감정 기반 대화": "💬 **감정 기반 대화**  \n\n대화할 내용을 입력해주세요.  \n\n오늘 하루 어땠나요? 당신의 이야기를 잘 들어주고 공감해줄 거예요.  \n\n재미있게 대화를 나눠보세요.",
        "실시간 정보 검색": "🌐 **실시간 정보 검색**  \n\n실시간 정보를 검색하기 위한 질문을 입력해주세요.  \n\n최신 뉴스, 지역 맛집, 날씨 등 최신 업데이트 내용에 대해서도 질문이 가능합니다.",
    }

    # 선택된 기능에 맞는 설명 출력
    if chain_type != "선택하지 않음":
        description = function_descriptions.get(chain_type, "")
        if description:
            st.markdown(f"#### 선택된 기능은 다음과 같습니다.\n\n\n{description}")

    # 대화 내용 초기화 버튼
    if st.button("대화 내용 초기화"):
        for key in st.session_state["messages"]:
            st.session_state["messages"][key].clear()
        st.session_state["chain"] = None
        st.session_state["current_function"] = None
        st.session_state["initial_message_shown"] = False
        st.session_state["user_input"] = ""

# 초기 안내 메시지
if not st.session_state["current_function"]:
    initial_message = """
    ### 안녕하세요, 저는 **MultiMinds** 입니다!

    "MultiMinds"는 "Multi"의 "다양한", "여러가지"와 "Minds"의 "지능", "사람들의 생각"에서 비롯된 이름입니다.   
    다양한 기능을 통합하여 사용자에게 폭넓은 지원을 제공하는 챗봇입니다.\n\n
    ---
    #### 사용하려는 기능을 왼쪽에서 선택해주세요.
    기능을 선택한 후, 질문을 입력해주세요.\n\n
    1️⃣  **문서 검색**: 원하는 내용의 문서의 경로를 찾고, 찾는 문서가 맞는지 간단한 내용을 보고 싶어요.\n
    2️⃣  **지원자 이력서**: 지원자 '김수현'의 이력서를 살펴보고 싶어요. 더불어 자기소개서, 경력사항, 수상 경력, 학력, 프로젝트 등에 대해 자세히 보고 싶어요.\n
    3️⃣  **대화 기능**: 대화를 나눌 사람이 필요해요. 오늘 있었던 일, 혹은 궁금한 점에 대한 질문과 대화를 나눠볼래요.\n
    4️⃣  **실시간 정보**: 최신 업데이트 내용에 대해서도 질문하고 싶어요. 현재 서울 날씨, 신촌 맛집, 최신 뉴스 등 실시간 정보가 궁금해요.\n
    """
    st.markdown(initial_message)

# 기능이 선택된 경우에만 입력창과 전송 버튼 표시
if st.session_state["current_function"] and st.session_state["chain"]:
    # 대화 기록 출력
    print_history()

    # 입력 바와 전송 버튼을 상단에 고정시키기 위한 CSS 추가
    st.markdown(
        """
        <style>
            /* 입력 바와 전송 버튼을 상단에 고정 */
            .input-container {
                display: flex;
                align-items: center;
                position: fixed;
                top: 0;
                width: 100%;
                padding: 10px;
                background: white;
                box-shadow: 0 1px 5px rgba(0,0,0,0.1);
                z-index: 10;
            }

            /* 텍스트 입력 영역 스타일 */
            .input-container .stTextArea {
                flex: 1;
                margin-right: 10px;
            }

            /* 전송 버튼 스타일 */
            .input-container .stButton {
                width: 100px;
                height: 100%;
                padding: 10px;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # 사용자 입력 처리
    with st.container():
        # 입력 바와 전송 버튼을 상단에 함께 배치
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        user_input = st.text_area(
            "입력하세요:",
            value=st.session_state["user_input"],
            height=30,
            key="input_area",
        )

        # 전송 버튼 클릭 시 처리
        if st.button("전송", key="send_button"):
            if user_input:
                st.session_state["user_input"] = ""  # 입력 필드 초기화
                if st.session_state["chain"]:
                    chain = st.session_state["chain"]
                    try:
                        response = chain(user_input)
                        add_history("user", user_input)
                        add_history("assistant", response)

                        # 사용자 입력과 응답을 점진적으로 출력
                        st.chat_message("user").markdown(user_input)
                        type_out_text(response)

                    except Exception as e:
                        error_message = f"❌ 오류가 발생했습니다: {str(e)}"
                        add_history("user", user_input)
                        add_history("assistant", error_message)

                        # 사용자 입력과 오류 메시지를 점진적으로 출력
                        st.chat_message("user").markdown(user_input)
                        type_out_text(error_message)
                else:
                    st.chat_message("assistant").markdown(
                        "⚠️ 기능이 설정되지 않았습니다."
                    )
        st.markdown("</div>", unsafe_allow_html=True)
