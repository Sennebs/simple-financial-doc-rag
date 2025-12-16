import os
import random

from pipelines.generation_pipeline import generate_answer
from pipelines.ingestion_pipeline import run_ingestion_pipeline
from ui.gradio_app import launch_gradio_app


def main(run_ingestion: bool = False):
    if run_ingestion:
        run_ingestion_pipeline()

    launch_gradio_app()


if __name__ == "__main__":
    # Run ingestion only once (the very first time)
    if not os.path.exists("./db/chroma_db"):
        main(run_ingestion=True)
    else:
        main(run_ingestion=False)
