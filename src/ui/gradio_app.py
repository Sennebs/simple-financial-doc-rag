import random
from pathlib import Path

import gradio as gr

from pipelines.generation_pipeline import generate_answer

CSS_PATH = Path(__file__).parent / "index.css"

EXAMPLE_QUESTIONS = [
    "How did Apple’s revenue change compared to the previous year?",
    "What were Tesla’s key profitability drivers in the most recent fiscal year?",
    "Which company reported the highest net income?",
    "How do these companies describe their cost structure?",
    "What factors influenced operating income across these companies?",
    "What are the main risk factors mentioned in Tesla's annual report?",
    "What operational risks does AB InBev highlight?",
    "What regulatory and legal risks does Alphabet identify?",
    "How does Nvidia describe competitive risks in its industry?",
    "What macroeconomic risks affect these companies’ performance?",
    "How does Nvidia position AI as a long-term growth driver?",
    "What future growth opportunities does Alphabet highlight?",
    "How does Tesla describe its long-term strategy?",
    "What strategic priorities does Apple emphasize?",
    "How do these companies plan to sustain competitive advantage?",
    "How does Nvidia describe its AI and data center strategy?",
    "How does Alphabet integrate AI into its products and services?",
    "What role does innovation play in Tesla’s business model?",
    "How does Apple describe its investment in research and development?",
    "Which company emphasizes AI infrastructure investments the most?",
    "How do these companies describe their capital expenditure plans?",
    "What investments does Tesla prioritize for future growth?",
    "How does Apple allocate cash toward shareholders?",
    "What role does R&D spending play across these companies?",
    "How does Alphabet justify its infrastructure investments?",
    "How do Apple and Alphabet differ in their growth strategies?",
    "Which company appears most exposed to regulatory risk?",
    "Which company relies most heavily on AI for future growth?",
    "How do these companies approach risk management differently?",
    "What similarities exist in how these companies describe future growth?",
]


def launch_gradio_app():

    def ensure_question(question: str):
        if question:
            return question.strip()
        return random.choice(EXAMPLE_QUESTIONS)

    def ask_question(question: str):
        result = generate_answer(question)

        answer = result.get("answer", "")
        sources = result.get("sources", [])
        source_text = "\n".join(sorted({src.split("/")[-1] for src in sources}))

        return answer, source_text

    with gr.Blocks(title="Simple Financial Document RAG", css=CSS_PATH.read_text()) as demo:
        gr.Markdown(
            """
            # Simple Financial Document RAG
            Ask questions about company annual reports (Apple, Nvidia, Tesla, Alphabet, AB InBev).
            """
        )

        with gr.Row():
            question_input = gr.Textbox(
                label="Enter your question", placeholder="Type a question or pick a random one", scale=1
            )

        with gr.Row():
            random_button = gr.Button("Pick a random question")
            ask_button = gr.Button("Ask")

        answer_output = gr.Textbox(label="Answer", lines=10, interactive=False)
        sources_output = gr.Textbox(label="Sources", lines=5, interactive=False)

        random_button.click(lambda: random.choice(EXAMPLE_QUESTIONS), outputs=[question_input])
        ask_button.click(ensure_question, inputs=[question_input], outputs=[question_input]).then(
            ask_question, inputs=[question_input], outputs=[answer_output, sources_output]
        )

    demo.launch()
