# Financial Document RAG (Retrieval-Augmented Generation)

A powerful portfolio project demonstrating how to build a Retrieval-Augmented Generation (RAG) system specialized for financial documents (Annual Reports). This application allows users to ask complex questions about financial performance, risks, and strategies across multiple companies (Apple, NVIDIA, Tesla, Alphabet, AB InBev) and receive accurate, source-cited answers.

## 🚀 Features

*   **Financial Domain Specialization**: Tailored to process and understand annual reports (PDFs).
*   **RAG Architecture**: Uses ChromaDB for vector storage and Groq (Llama 3) for high-speed, accurate generation.
*   **Intelligent Chunking**: Custom chunking strategy ensuring page-level citations.
*   **Interactive UI**: Modern, clean web interface built with **Gradio**.
*   **Source Citations**: Every answer includes precise references to the source document and page number.

## 🛠️ Tech Stack

*   **Language**: Python 3.10+
*   **LLM**: [Groq](https://groq.com/) (Llama 3.3 70B Versatile) for ultra-fast inference.
*   **Vector Database**: [ChromaDB](https://www.trychroma.com/) (local persistent storage).
*   **Embeddings**: HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`).
*   **UI Framework**: [Gradio](https://www.gradio.app/).
*   **PDF Processing**: PyMuPDF.

## 📂 Project Structure

```bash
financial-document-rag/
├── data/
│   └── raw/                    # Place your PDF annual reports here
├── src/
│   ├── db/                     # Vector store location (ignored in git)
│   ├── pipelines/              # Core logic
│   │   ├── ingestion.py        # Processes PDFs and builds vector DB
│   │   ├── retrieval.py        # Searches for relevant chunks
│   │   └── generation.py       # Generates answers with LLM
│   ├── ui/
│   │   └── gradio_app.py       # Web interface entry point
│   ├── utils/
│   │   └── chunking.py         # Chunking utilities
│   │   └── pdf_processing.py   # PDF processing utilities
│   │   └── vector_store.py     # Vector store utilities
│   └── main.py                 # CLI entry point
├── .env.example                # Template for environment variables
└── requirements.txt            # Project dependencies
```

## ⚡ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/financial-document-rag.git
cd financial-document-rag
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
Open `.env` and add your keys. Note that `RAW_DATA_DIR` should be relative to `src` (e.g., `../data/raw`) if running from there:
```ini
GROQ_API_KEY=your_groq_api_key_here
RAW_DATA_DIR=../data/raw
```

### 5. Run the Application
The application handles data ingestion automatically. If the vector database doesn't exist, it will run the ingestion pipeline first.

Navigate to the `src` directory and run the main entry point:
```bash
cd src
python main.py
```

*   **First Run**: The app will verify data, process PDFs from `../data/raw`, and build the Vector DB (this may take a minute).
*   **Subsequent Runs**: It will skip ingestion and launch the UI immediately.

The Gradio interface will open in your browser (usually at `http://127.0.0.1:7860`).

## 🧠 How It Works

1.  **Ingestion**: The system reads PDF files, extracts text page-by-page, and cleans it.
2.  **Chunking**: Text is split into manageable chunks while preserving metadata (Company, Year, Page Number).
3.  **Embedding**: Chunks are converted into vector embeddings using `all-MiniLM-L6-v2`.
4.  **Retrieval**: When you ask a question, the system finds the most similar chunks in the vector store.
5.  **Generation**: The retrieved context + your question are sent to the Groq LLM, which synthesizes an answer with citations.

## ⚠️ Note on "Empty Database" Issues
If you encounter an issue where no documents are retrieved, ensure you run the ingestion script **from the src folder** or ensure the path to `db/chroma_db` is consistent. The project is configured to look for the database in `db/chroma_db` relative to the execution context.

