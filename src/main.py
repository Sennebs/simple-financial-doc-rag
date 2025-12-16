import random

from pipelines.generation_pipeline import generate_answer
from pipelines.ingestion_pipeline import run_ingestion_pipeline

if __name__ == "__main__":
    # Run ingestion once
    # run_ingestion_pipeline()

    EXAMPLE_QUESTIONS = [
        "What are the main risk factors mentioned in Tesla's annual report?",
        "How does Apple describe its revenue streams?",
        "What regulatory risks does Alphabet highlight?",
        "How does Nvidia position AI as a growth driver?",
        "What are the main operational risks for AB InBev?",
        "Which company emphasizes AI infrastructure investments the most?",
        "How do these companies describe future growth opportunities?",
    ]

    query = random.choice(EXAMPLE_QUESTIONS)

    result = generate_answer(query)
    print("Answer:", result)
