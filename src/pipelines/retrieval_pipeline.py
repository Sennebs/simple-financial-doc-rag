import logging

import config.logging_config
from utils.vector_store import load_vector_store

logger = logging.getLogger(__name__)


def create_retriever(vector_store, k: int = 5):
    """
    Creates a retriever from the vector store.
    """
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    return retriever


def retrieve_documents(query: str, k: int = 5):
    """
    Retrieves the top k documents most similar to the query.
    """
    vector_store = load_vector_store()
    retriever = create_retriever(vector_store, k)

    logger.info(f"Retrieving top {k} documents for query: {query}")

    docs = retriever.invoke(query)
    return docs
