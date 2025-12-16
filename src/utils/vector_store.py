import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def create_embeddings():
    """
    Creates an embedding function using Google Generative AI.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_vector_store(chunks: list[Document], persist_directory: str = "db/chroma_db"):
    """
    Create and persist a vector store using ChromaDB.
    """

    embeddings = create_embeddings()

    # Create ChromaDB vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="financial-documents",
    )

    return vector_store


def load_vector_store(persist_directory: str = "db/chroma_db"):
    """
    Load a vector store from a disk.
    """
    embeddings = create_embeddings()
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name="financial-documents",
    )

    return vector_store
