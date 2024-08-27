from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 경로 설정
summary_vectorstore_path = (
    "/Users/kimsoohyun/Desktop/eeve_model/src/vectore_store/summary_faiss"
)
resume_vectorstore_path = (
    "/Users/kimsoohyun/Desktop/eeve_model/src/vectore_store/resume_faiss"
)

# 임베딩 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", disallowed_special=())


def load_resume_retriever():
    """
    이력서에 대한 FAISS 벡터 스토어에서 retriever를 생성하는 함수.
    """
    resume_db = FAISS.load_local(
        resume_vectorstore_path, embeddings, allow_dangerous_deserialization=True
    )
    resume_retriever = resume_db.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    )
    return resume_retriever


def load_summary_retriever():
    """
    요약문에 대한 FAISS 벡터 스토어에서 retriever를 생성하는 함수.
    """
    summary_db = FAISS.load_local(
        summary_vectorstore_path, embeddings, allow_dangerous_deserialization=True
    )
    summary_retriever = summary_db.as_retriever(
        search_type="similarity", search_kwargs={"k": 10}
    )
    return summary_retriever


resume_retriever = load_resume_retriever()
summary_retriever = load_summary_retriever()

__all__ = ["summary_retriever", "resume_retriever"]
