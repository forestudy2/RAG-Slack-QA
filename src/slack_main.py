import os
from chain import summary_chain, resume_chain, conversation_chain, search_chain
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

user_sessions = {}  # 사용자별 세션을 관리하는 딕셔너리


def greet_user():
    return {
        "text": "*안녕하세요! 무엇을 도와드릴까요? 💬*",
        "blocks": [
            {
                "type": "section",
                "block_id": "greeting_section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "*안녕하세요! 무엇을 도와드릴까요? 💬*\n"
                        "*저는 다음과 같은 기능이 있습니다. 사용하려는 `기능의 번호`를 입력해주세요.*\n\n"
                        "1️⃣ *문서 검색:* 원하는 내용의 문서를 찾고, 간단한 내용을 보고 싶어요.\n"
                        "2️⃣ *지원자 이력서:* 지원자 '김수현'의 이력서를 살펴보고 싶어요.\n"
                        "3️⃣ *대화 기능:* 대화를 나눌 사람이 필요해요. 대화를 나눠볼래요.\n"
                        "4️⃣ *실시간 정보:* 현재 서울 날씨나 신촌 맛집 같은 실시간 정보가 궁금해요.\n\n"
                        "*기능의 번호를 입력한 후, 질문을 입력해주세요.*\n\n"
                        "*대화의 기능을 변경하고 싶으시면 `대화 내용 변경`을 입력해주시고,*\n"
                        "*대화를 그만하고 싶으시면 `대화 그만하기`를 입력해주세요.*"
                    ),
                },
            }
        ],
    }


def explain_function_and_prompt(chain_type):
    explanations = {
        "1": "*📄 문서 검색 기능입니다.* 문서 내용을 찾기 위한 *질문을 입력해주세요.*",
        "2": "*👤 지원자 이력서 기능입니다.* 지원자 '김수현'의 이력서를 보기 위한 *질문을 입력해주세요.*",
        "3": "*💬 대화 기능입니다. 대화할 내용을 입력해주세요.*",
        "4": "*🌐 실시간 정보 검색 기능입니다.* 실시간 정보를 검색하기 위한 *질문을 입력해주세요.*",
    }
    return {
        "text": f"*기능 '{chain_type}'이 선택되었습니다.*",
        "blocks": [
            {
                "type": "section",
                "block_id": f"function_{chain_type}",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*기능 '{chain_type}'이 선택되었습니다.*\n{explanations.get(chain_type, '*해당 기능에 대한 설명이 없습니다.*')}",
                },
            }
        ],
    }


def handle_function_change():
    return {
        "text": "*🔄 대화 내용을 변경하겠습니다. 다시 기능 번호를 입력해주세요.*",
        "blocks": [
            {
                "type": "section",
                "block_id": "change_function",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "*🔄 대화 내용을 변경하겠습니다. 다시 기능 번호를 입력해주세요.*\n\n"
                        "1️⃣ *문서 검색:* 원하는 내용의 문서를 찾고, 간단한 내용을 보고 싶어요.\n"
                        "2️⃣ *지원자 이력서:* 지원자 '김수현'의 이력서를 살펴보고 싶어요.\n"
                        "3️⃣ *대화 기능:* 대화를 나눌 사람이 필요해요. 대화를 나눠볼래요.\n"
                        "4️⃣ *실시간 정보:* 현재 서울 날씨나 신촌 맛집 같은 실시간 정보가 궁금해요.\n\n"
                        "*기능의 번호를 입력한 후, 질문을 입력해주세요.*"
                    ),
                },
            }
        ],
    }


def end_conversation():
    return {
        "text": "*👋 대화를 종료하겠습니다. 필요하시면 언제든지 다시 연락주세요!*",
        "blocks": [
            {
                "type": "section",
                "block_id": "end_conversation",
                "text": {
                    "type": "mrkdwn",
                    "text": "*👋 대화를 종료하겠습니다. 필요하시면 언제든지 다시 연락주세요!*",
                },
            }
        ],
    }


def execute_chain(chain_type, query):
    if chain_type == "1":
        response = summary_chain(query)
    elif chain_type == "2":
        response = resume_chain(query)
    elif chain_type == "3":
        response = conversation_chain(query)
    elif chain_type == "4":
        response = search_chain(query)
    else:
        response = "*⚠️ 잘못된 입력입니다. 다시 시도해 주세요.*"
    return {
        "text": response,
        "blocks": [
            {
                "type": "section",
                "block_id": f"response_{chain_type}",
                "text": {"type": "mrkdwn", "text": response},
            }
        ],
    }


@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    user_id = body["event"]["user"]
    message = body["event"]["text"].strip().replace(" ", "")

    # 세션이 없는 경우 초기화
    if user_id not in user_sessions:
        user_sessions[user_id] = None

    if message.lower() in ["대화내용변경", "대화그만하기"]:
        if message.lower() == "대화내용변경":
            response = handle_function_change()
        elif message.lower() == "대화그만하기":
            response = end_conversation()
        user_sessions[user_id] = None  # 사용자 세션 초기화
    elif message.startswith(("1", "2", "3", "4")):
        chain_type = message[0]
        user_sessions[user_id] = chain_type  # 사용자 세션 업데이트
        response = explain_function_and_prompt(chain_type)
    elif user_sessions[user_id]:
        chain_type = user_sessions[user_id]
        response = execute_chain(chain_type, message)
    else:
        response = greet_user()

    say(**response)


@app.message(".*")
def message_handler(message, say, logger):
    user_id = message["user"]
    text = message["text"].strip().replace(" ", "")

    # 세션이 없는 경우 초기화
    if user_id not in user_sessions:
        user_sessions[user_id] = None

    if text.lower() in ["대화내용변경", "대화그만하기"]:
        if text.lower() == "대화내용변경":
            response = handle_function_change()
        elif text.lower() == "대화그만하기":
            response = end_conversation()
        user_sessions[user_id] = None  # 사용자 세션 초기화
    elif text.startswith(("1", "2", "3", "4")):
        chain_type = text[0]
        user_sessions[user_id] = chain_type  # 사용자 세션 업데이트
        response = explain_function_and_prompt(chain_type)
    elif user_sessions[user_id]:
        chain_type = user_sessions[user_id]
        response = execute_chain(chain_type, text)
    else:
        response = greet_user()

    say(**response)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()