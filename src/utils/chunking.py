import logging

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config.logging_config

logger = logging.getLogger(__name__)


def chunk_text(full_text_dict: dict[str, str], chunk_size: int = 1500, chunk_overlap: int = 200):
    """
    Splits a text into chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " "],
        add_start_index=True,
        strip_whitespace=True,
    )

    doc = Document(page_content=full_text_dict["full_text"], metadata=full_text_dict["metadata"])
    chunks = splitter.split_documents([doc])

    logger.info(f"Split document into {len(chunks)} chunks")
    return chunks
