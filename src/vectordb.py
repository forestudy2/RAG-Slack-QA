import os
import re
import json
import numpy as np
from sklearn.cluster import KMeans
from langchain import hub
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 경로 설정
pdf_folder_path = "/Users/kimsoohyun/Desktop/eeve_model/src/data/notion_pdf"
resume_pdf_path = "/Users/kimsoohyun/Desktop/eeve_model/src/data/notion_resume.pdf"
summary_json_path = "/Users/kimsoohyun/Desktop/eeve_model/src/summary_data.json"
summary_vectorstore_path = "/Users/kimsoohyun/Desktop/eeve_model/src/vectore_store/summary_faiss"
resume_vectorstore_path = "/Users/kimsoohyun/Desktop/eeve_model/src/vectore_store/resume_faiss"

# 임베딩 및 LLM 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", disallowed_special=())
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


def process_pdf(pdf_file, base_folder):
    """PDF 로드, 전처리, 텍스트 청크 생성, 클러스터링, 요약문 생성"""
    loader = PDFMinerLoader(pdf_file)
    docs = loader.load()
    if not docs:
        return None, None

    text = "\n\n".join([doc.page_content for doc in docs])
    text = text.replace("\x0c", " ")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r" +", " ", text)
    text = text.strip()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    text_chunks = text_splitter.split_text(text)
    vectors = embeddings.embed_documents(text_chunks)

    if len(vectors) <= 1:
        selected_docs = [Document(page_content=chunk) for chunk in text_chunks]
    else:
        num_clusters = min(max(len(vectors) // 2, 1), 10)
        kmeans = KMeans(n_clusters=num_clusters, random_state=123).fit(vectors)
        closest_indices = [
            np.argmin(np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1))
            for i in range(num_clusters)
        ]
        selected_docs = [
            Document(page_content=text_chunks[idx]) for idx in sorted(closest_indices)
        ]

    map_summary = hub.pull("teddynote/map-summary-prompt")
    map_chain = map_summary | llm | StrOutputParser()
    input_doc = [
        {"documents": doc.page_content, "language": "Korean"} for doc in selected_docs
    ]
    summaries = map_chain.batch(input_doc)

    relative_path = os.path.relpath(pdf_file, base_folder)
    return summaries, relative_path


def generate_summaries_and_save(pdf_folder, summary_json_path):
    """PDF 파일을 처리하여 요약문 생성 후, JSON 파일로 저장"""
    if os.path.exists(summary_json_path):
        with open(summary_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        doc_paths = data.get("doc_paths", {})
        document_summaries = data.get("document_summaries", {})
    else:
        doc_paths = {}
        document_summaries = {}

    pdf_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(pdf_folder)
        for file in files
        if file.endswith(".pdf")
    ]

    for pdf_file in pdf_files:
        relative_path = os.path.relpath(pdf_file, pdf_folder)
        if relative_path not in doc_paths:
            summaries, path = process_pdf(pdf_file, pdf_folder)
            if summaries:
                document_summaries[path] = summaries
                doc_paths[path] = path

    data = {"doc_paths": doc_paths, "document_summaries": document_summaries}
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return document_summaries, doc_paths


def create_resume_vectorstore(resume_pdf_path, resume_vectorstore_path):
    """
    이력서 PDF를 기반으로 벡터 스토어를 생성하고 로컬에 저장하는 함수
    """
    loader = PDFMinerLoader(resume_pdf_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["#", "##", "###", "\n\n", "\n", "."],
        chunk_size=1500,
        chunk_overlap=100,
    )
    split_documents = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
    vectorstore.save_local(resume_vectorstore_path)


def create_summary_vectorstore(pdf_folder, summary_json_path, summary_vectorstore_path):
    """
    PDF 문서에서 요약문을 생성하고 이를 기반으로 벡터 스토어를 생성한 뒤 로컬에 저장하는 함수.
    """
    document_summaries, doc_paths = generate_summaries_and_save(
        pdf_folder, summary_json_path
    )

    documents = [
        Document(page_content="".join(summary), metadata={"pdf": path})
        for summary, path in zip(document_summaries.values(), doc_paths.keys())
    ]

    if not documents:
        print("Error: No documents to create vectorstore.")
        return

    vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)
    vectorstore.save_local(summary_vectorstore_path)


if __name__ == "__main__":
    create_resume_vectorstore(resume_pdf_path, resume_vectorstore_path)
    create_summary_vectorstore(
        pdf_folder_path, summary_json_path, summary_vectorstore_path
    )
