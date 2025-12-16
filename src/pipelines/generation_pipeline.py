import logging

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

import config.logging_config
from pipelines.retrieval_pipeline import retrieve_documents

load_dotenv()

logger = logging.getLogger(__name__)


def format_documents(documents: list[Document]):
    """
    Formats a list of documents into a single string with source markers.
    """
    context = []
    sources = []

    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "Unknown Source")

        context.append(f"Source {i}: {source}\n{doc.page_content}")
        sources.append(source)

    return "\n\n".join(context), sorted(set(sources))


def generate_answer(query: str, k: int = 5):
    """
    Generates an answer to a query using the retrieved documents and Groq LLM.
    """
    logger.info(f"Generating answer for query: {query}")

    documents = retrieve_documents(query, k)
    if not documents:
        logger.warning(f"No documents retrieved for query: {query}")
        return ""

    context, sources = format_documents(documents)

    system_prompt = (
        "You are a helpful assistant answering questions based on internal documents.\n"
        "Use ONLY the provided context to answer the question.\n"
        "If the answer is not in the context, say you do not know.\n"
        "Be concise, factual, and professional.\n"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Context:\n{context}\n\nQuestion:\n{query}"),
        ]
    )

    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
    parser = StrOutputParser()

    chain = prompt | llm | parser

    answer = chain.invoke({"context": context, "query": query})

    return {"answer": answer.strip(), "sources": sources}
