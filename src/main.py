import os
from chain import summary_chain, resume_chain, conversation_chain, search_chain
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# def greet_user():
#     print("안녕하세요! 무엇을 도와드릴까요? 💬✨")
#     print("저는 다음과 같은 기능이 있습니다. 사용하려는 기능의 번호를 입력해주세요.")
#     print("대화를 나누다가 기능을 변경하고 싶다면 '대화 내용 변경'을 입력해주세요.")
#     print("대화를 그만하고 싶다면 '대화 그만하기'를 입력해주세요.")
#     print()
#     print("1. 원하는 내용의 문서를 찾고, 찾는 문서가 맞는지 간단한 내용을 보고싶어요.")
#     print("2. 지원자 '김수현'이 누군지 궁금합니다. 간단한 이력서를 살펴보고 싶어요.")
#     print("3. 대화를 나눌 사람이 필요해요. 대화를 나눠볼래요.")
#     print("4. 실시간 정보가 궁금해요. ex) 현재 서울 날씨는?, 대표적 신촌 맛집은? ")


# def execute_chain(chain_type, query):
#     if chain_type == "1":
#         response = summary_chain(query)
#     elif chain_type == "2":
#         response = resume_chain(query)
#     elif chain_type == "3":
#         response = conversation_chain(query, session_id="default_session")
#     elif chain_type == "4":
#         response = search_chain(query)
#     else:
#         response = "잘못된 입력입니다. 다시 시도해 주세요."
#     return response


# def main():
#     current_chain = None

#     while True:
#         if current_chain is None:
#             greet_user()
#             current_chain = input("원하는 기능의 번호를 입력하세요: ")

#         if current_chain in ["1", "2", "3", "4"]:
#             query = input("질문을 입력하세요: ")
#             if query.lower() == "대화 내용 변경":
#                 current_chain = None
#                 continue
#             elif query.lower() == "대화 그만하기":
#                 print("대화를 종료합니다. 감사합니다! 👋")
#                 break

#             response = execute_chain(current_chain, query)
#             print(f"Response:\n{response}\n")

#         else:
#             print("잘못된 입력입니다. 다시 시도해 주세요.")
#             current_chain = None


# if __name__ == "__main__":
#     main()


# Initialize user_sessions to track active sessions
# user_sessions = {}


# # Function definitions
# def greet_user():
#     return (
#         "안녕하세요! 무엇을 도와드릴까요? 💬✨\n"
#         "저는 다음과 같은 기능이 있습니다. 사용하려는 기능의 번호를 입력해주세요.\n"
#         "1: 원하는 내용의 문서를 찾고, 찾는 문서가 맞는지 간단한 내용을 보고싶어요.\n"
#         "2: 지원자 '김수현'이 누군지 궁금합니다. 간단한 이력서를 살펴보고 싶어요.\n"
#         "3: 대화를 나눌 사람이 필요해요. 대화를 나눠볼래요.\n"
#         "4: 실시간 정보가 궁금해요. ex) 현재 서울 날씨는?, 대표적 신촌 맛집은?\n\n"
#         "기능을 선택하신 후, 질문을 입력해주세요."
#     )


# def explain_function_and_prompt(chain_type):
#     explanations = {
#         "1": "문서 검색 기능입니다. 문서 내용을 찾기 위한 질문을 입력해주세요.",
#         "2": "지원자 이력서 기능입니다. 지원자 '김수현'의 이력서를 보기 위한 질문을 입력해주세요.",
#         "3": "대화 기능입니다. 대화할 내용을 입력해주세요.",
#         "4": "실시간 정보 검색 기능입니다. 실시간 정보를 검색하기 위한 질문을 입력해주세요.",
#     }
#     return f"기능 '{chain_type}'이 선택되었습니다. {explanations.get(chain_type, '해당 기능에 대한 설명이 없습니다.')}\n질문을 입력해주세요."


# def handle_function_change():
#     return "대화 내용을 변경하겠습니다. 다시 기능 번호를 입력해주세요."


# def end_conversation():
#     return "대화를 종료하겠습니다. 필요하시면 언제든지 다시 연락주세요!"


# def execute_chain(chain_type, query):
#     if chain_type == "1":
#         return summary_chain(query)
#     elif chain_type == "2":
#         return resume_chain(query)
#     elif chain_type == "3":
#         return conversation_chain(query)
#     elif chain_type == "4":
#         return search_chain(query)
#     else:
#         return "잘못된 입력입니다. 다시 시도해 주세요."


# @app.event("app_mention")
# def handle_app_mention_events(body, say, logger):
#     user_id = body["event"]["user"]
#     message = body["event"]["text"].strip()

#     # Handle messages for function change or end conversation
#     if message in ["대화 내용 변경", "대화 그만하기"]:
#         if message.lower() == "대화 내용 변경":
#             response = handle_function_change()
#         elif message.lower() == "대화 그만하기":
#             response = end_conversation()
#         # Reset conversation context
#         user_sessions[user_id] = None
#     # Handle function selection
#     elif (
#         message.startswith("1")
#         or message.startswith("2")
#         or message.startswith("3")
#         or message.startswith("4")
#     ):
#         chain_type = message[0]
#         user_sessions[user_id] = chain_type  # Save the selected function
#         response = explain_function_and_prompt(chain_type)
#     # Handle user query based on the selected function
#     elif user_id in user_sessions and user_sessions[user_id]:
#         chain_type = user_sessions[user_id]
#         response = execute_chain(chain_type, message)
#     else:
#         response = greet_user()
#         user_sessions[user_id] = None  # Set default state

#     say(response)


# @app.message(".*")
# def message_handler(message, say, logger):
#     user_id = message["user"]
#     text = message["text"].strip()

#     # Handle messages for function change or end conversation
#     if text in ["대화 내용 변경", "대화 그만하기"]:
#         if text.lower() == "대화 내용 변경":
#             response = handle_function_change()
#         elif text.lower() == "대화 그만하기":
#             response = end_conversation()
#         # Reset conversation context
#         user_sessions[user_id] = None
#     # Handle function selection
#     elif (
#         text.startswith("1")
#         or text.startswith("2")
#         or text.startswith("3")
#         or text.startswith("4")
#     ):
#         chain_type = text[0]
#         user_sessions[user_id] = chain_type  # Save the selected function
#         response = explain_function_and_prompt(chain_type)
#     # Handle user query based on the selected function
#     elif user_id in user_sessions and user_sessions[user_id]:
#         chain_type = user_sessions[user_id]
#         response = execute_chain(chain_type, text)
#     else:
#         response = greet_user()
#         user_sessions[user_id] = None  # Set default state

#     say(response)


# if __name__ == "__main__":
#     SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


# user_sessions = {}


# # Function definitions
# def greet_user():
#     return (
#         "*안녕하세요! 무엇을 도와드릴까요? 💬✨*\n"
#         "*저는 다음과 같은 기능이 있습니다. 사용하려는 기능의 번호를 입력해주세요.*\n"
#         "*1:* 원하는 내용의 문서를 찾고, 찾는 문서가 맞는지 간단한 내용을 보고싶어요.\n"
#         "*2:* 지원자 '김수현'이 누군지 궁금합니다. 간단한 이력서를 살펴보고 싶어요.\n"
#         "*3:* 대화를 나눌 사람이 필요해요. 대화를 나눠볼래요.\n"
#         "*4:* 실시간 정보가 궁금해요. ex) 현재 서울 날씨는?, 대표적 신촌 맛집은? \n\n"
#         "*기능을 선택하신 후, 질문을 입력해주세요.*"
#     )


# def explain_function_and_prompt(chain_type):
#     explanations = {
#         "1": "*문서 검색 기능입니다.* 문서 내용을 찾기 위한 질문을 입력해주세요.",
#         "2": "*지원자 이력서 기능입니다.* 지원자 '김수현'의 이력서를 보기 위한 질문을 입력해주세요.",
#         "3": "*대화 기능입니다.* 대화할 내용을 입력해주세요.",
#         "4": "*실시간 정보 검색 기능입니다.* 실시간 정보를 검색하기 위한 질문을 입력해주세요.",
#     }
#     return f"*기능 '{chain_type}'이 선택되었습니다.* {explanations.get(chain_type, '*해당 기능에 대한 설명이 없습니다.*')}\n*질문을 입력해주세요.*"


# def handle_function_change():
#     return "*대화 내용을 변경하겠습니다. 다시 기능 번호를 입력해주세요.*"


# def end_conversation():
#     return "*대화를 종료하겠습니다. 필요하시면 언제든지 다시 연락주세요!*"


# def execute_chain(chain_type, query):
#     if chain_type == "1":
#         response = summary_chain(query)
#     elif chain_type == "2":
#         response = resume_chain(query)
#     elif chain_type == "3":
#         response = conversation_chain(query)
#     elif chain_type == "4":
#         response = search_chain(query)
#     else:
#         response = "*잘못된 입력입니다. 다시 시도해 주세요.*"
#     return response


# @app.event("app_mention")
# def handle_app_mention_events(body, say, logger):
#     user_id = body["event"]["user"]
#     message = body["event"]["text"].strip()

#     if message in ["대화 내용 변경", "대화 그만하기"]:
#         if message.lower() == "대화 내용 변경":
#             response = handle_function_change()
#         elif message.lower() == "대화 그만하기":
#             response = end_conversation()
#         user_sessions[user_id] = None
#     elif (
#         message.startswith("1")
#         or message.startswith("2")
#         or message.startswith("3")
#         or message.startswith("4")
#     ):
#         chain_type = message[0]
#         user_sessions[user_id] = chain_type
#         response = explain_function_and_prompt(chain_type)
#     elif user_id in user_sessions and user_sessions[user_id]:
#         chain_type = user_sessions[user_id]
#         response = execute_chain(chain_type, message)
#     else:
#         response = greet_user()
#         user_sessions[user_id] = None

#     say(response)


# @app.message(".*")
# def message_handler(message, say, logger):
#     user_id = message["user"]
#     text = message["text"].strip()

#     if text in ["대화 내용 변경", "대화 그만하기"]:
#         if text.lower() == "대화 내용 변경":
#             response = handle_function_change()
#         elif text.lower() == "대화 그만하기":
#             response = end_conversation()
#         user_sessions[user_id] = None
#     elif (
#         text.startswith("1")
#         or text.startswith("2")
#         or text.startswith("3")
#         or text.startswith("4")
#     ):
#         chain_type = text[0]
#         user_sessions[user_id] = chain_type
#         response = explain_function_and_prompt(chain_type)
#     elif user_id in user_sessions and user_sessions[user_id]:
#         chain_type = user_sessions[user_id]
#         response = execute_chain(chain_type, text)
#     else:
#         response = greet_user()
#         user_sessions[user_id] = None

#     say(response)


# if __name__ == "__main__":
#     SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


# Initialize user_sessions to track active sessions
user_sessions = {}


def greet_user():
    return {
        "text": "*안녕하세요! 무엇을 도와드릴까요? 💬✨*",
        "blocks": [
            {
                "type": "section",
                "block_id": "greeting_section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*안녕하세요! 무엇을 도와드릴까요? 💬✨*\n\n"
                    "*저는 다음과 같은 기능이 있습니다. 사용하려는 기능의 번호를 입력해주세요.*\n"
                    "*1:* 원하는 내용의 문서를 찾고, 찾는 문서가 맞는지 간단한 내용을 보고싶어요.\n"
                    "*2:* 지원자 '김수현'이 누군지 궁금합니다. 간단한 이력서를 살펴보고 싶어요.\n"
                    "*3:* 대화를 나눌 사람이 필요해요. 대화를 나눠볼래요.\n"
                    "*4:* 실시간 정보가 궁금해요. ex) 현재 서울 날씨는?, 대표적 신촌 맛집은? \n\n"
                    "*기능을 선택하신 후, 질문을 입력해주세요.*",
                },
            }
        ],
    }


def explain_function_and_prompt(chain_type):
    explanations = {
        "1": "*문서 검색 기능입니다.* 문서 내용을 찾기 위한 질문을 입력해주세요.",
        "2": "*지원자 이력서 기능입니다.* 지원자 '김수현'의 이력서를 보기 위한 질문을 입력해주세요.",
        "3": "*대화 기능입니다.* 대화할 내용을 입력해주세요.",
        "4": "*실시간 정보 검색 기능입니다.* 실시간 정보를 검색하기 위한 질문을 입력해주세요.",
    }
    return {
        "text": f"*기능 '{chain_type}'이 선택되었습니다.*",
        "blocks": [
            {
                "type": "section",
                "block_id": f"function_{chain_type}",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*기능 '{chain_type}'이 선택되었습니다.*\n{explanations.get(chain_type, '*해당 기능에 대한 설명이 없습니다.*')}\n*질문을 입력해주세요.*",
                },
            }
        ],
    }


def handle_function_change():
    return {
        "text": "*대화 내용을 변경하겠습니다. 다시 기능 번호를 입력해주세요.*",
        "blocks": [
            {
                "type": "section",
                "block_id": "change_function",
                "text": {
                    "type": "mrkdwn",
                    "text": "*대화 내용을 변경하겠습니다. 다시 기능 번호를 입력해주세요.*",
                },
            }
        ],
    }


def end_conversation():
    return {
        "text": "*대화를 종료하겠습니다. 필요하시면 언제든지 다시 연락주세요!*",
        "blocks": [
            {
                "type": "section",
                "block_id": "end_conversation",
                "text": {
                    "type": "mrkdwn",
                    "text": "*대화를 종료하겠습니다. 필요하시면 언제든지 다시 연락주세요!*",
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
        response = "*잘못된 입력입니다. 다시 시도해 주세요.*"
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
    message = body["event"]["text"].strip()

    if message.lower() in ["대화 내용 변경", "대화 그만하기"]:
        if message.lower() == "대화 내용 변경":
            response = handle_function_change()
        elif message.lower() == "대화 그만하기":
            response = end_conversation()
        user_sessions[user_id] = None
    elif message.startswith(("1", "2", "3", "4")):
        chain_type = message[0]
        user_sessions[user_id] = chain_type
        response = explain_function_and_prompt(chain_type)
    elif user_id in user_sessions and user_sessions[user_id]:
        chain_type = user_sessions[user_id]
        response = execute_chain(chain_type, message)
    else:
        response = greet_user()
        user_sessions[user_id] = None

    say(**response)


@app.message(".*")
def message_handler(message, say, logger):
    user_id = message["user"]
    text = message["text"].strip()

    if text.lower() in ["대화 내용 변경", "대화 그만하기"]:
        if text.lower() == "대화 내용 변경":
            response = handle_function_change()
        elif text.lower() == "대화 그만하기":
            response = end_conversation()
        user_sessions[user_id] = None
    elif text.startswith(("1", "2", "3", "4")):
        chain_type = text[0]
        user_sessions[user_id] = chain_type
        response = explain_function_and_prompt(chain_type)
    elif user_id in user_sessions and user_sessions[user_id]:
        chain_type = user_sessions[user_id]
        response = execute_chain(chain_type, text)
    else:
        response = greet_user()
        user_sessions[user_id] = None

    say(**response)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
