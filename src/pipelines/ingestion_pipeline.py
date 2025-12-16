import logging
import os

from dotenv import load_dotenv

import config.logging_config
from utils.chunking import chunk_text
from utils.pdf_processing import pdf_to_full_text
from utils.vector_store import create_vector_store

load_dotenv()

logger = logging.getLogger(__name__)

RAW_DATA_DIR = os.getenv("RAW_DATA_DIR")
PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR")


def run_ingestion_pipeline():
    logger.info("Starting ingestion pipeline")

    all_chunks = []

    for file_name in os.listdir(RAW_DATA_DIR):
        if not file_name.endswith(".pdf"):
            continue

        logger.debug(f"Processing file: {file_name}")
        pdf_path = os.path.join(RAW_DATA_DIR, file_name)
        # PDF into cleaned text
        full_text_dict = pdf_to_full_text(pdf_path)
        # Cleaned text into chunks
        chunks = chunk_text(full_text_dict)

        all_chunks.extend(chunks)

    if not all_chunks:
        logger.warning("No chunks created. Pipeline completed without processing any files.")
        return

    # Chunks into vector store
    logger.info("Creating vector store")
    vector_store = create_vector_store(chunks=all_chunks)

    logger.info("Ingestion pipeline completed successfully")
    return vector_store


if __name__ == "__main__":
    run_ingestion_pipeline()
