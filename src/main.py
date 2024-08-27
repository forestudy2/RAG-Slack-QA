from chain import summary_chain, resume_chain, conversation_chain


def greet_user():
    print("안녕하세요! 무엇을 도와드릴까요? 💬✨")
    print("저는 다음과 같은 기능이 있습니다. 사용하려는 기능의 번호를 입력해주세요.")
    print("대화를 나누다가 기능을 변경하고 싶다면 '대화 내용 변경'을 입력해주세요.")
    print("대화를 그만하고 싶다면 '대화 그만하기'를 입력해주세요.")
    print()
    print("1. 원하는 내용의 문서를 찾고, 찾는 문서가 맞는지 간단한 내용을 보고싶어요.")
    print("2. 지원자 '김수현'이 누군지 궁금합니다. 간단한 이력서를 살펴보고 싶어요.")
    print("3. 대화를 나눌 사람이 필요해요. 대화를 나눠볼래요.")


def execute_chain(chain_type, query):
    if chain_type == "1":
        response = summary_chain(query)
    elif chain_type == "2":
        response = resume_chain(query)
    elif chain_type == "3":
        response = conversation_chain(query, session_id="default_session")
    else:
        response = "잘못된 입력입니다. 다시 시도해 주세요."
    return response


def main():
    current_chain = None

    while True:
        if current_chain is None:
            greet_user()
            current_chain = input("원하는 기능의 번호를 입력하세요: ")

        if current_chain in ["1", "2", "3"]:
            query = input("질문을 입력하세요: ")
            if query.lower() == "대화 내용 변경":
                current_chain = None
                continue
            elif query.lower() == "대화 그만하기":
                print("대화를 종료합니다. 감사합니다! 👋")
                break

            response = execute_chain(current_chain, query)
            print(f"Response:\n{response}\n")

        else:
            print("잘못된 입력입니다. 다시 시도해 주세요.")
            current_chain = None


if __name__ == "__main__":
    main()
