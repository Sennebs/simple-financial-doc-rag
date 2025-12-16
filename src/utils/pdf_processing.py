import logging

import pymupdf

import config.logging_config

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> list[tuple[int, str]]:
    """
    Extracts text from a PDF and returns a list of tuples containing the page number and the text on that page.
    """
    logger.debug(f"Extracting text from PDF: {pdf_path}")
    doc = pymupdf.open(pdf_path)
    pages = []

    for page in doc:
        pages.append((page.number + 1, page.get_text("text")))
    doc.close()

    logger.debug(f"Extracted {len(pages)} pages from PDF")
    return pages


def clean_page_text(text: str) -> str:
    """
    Cleans the text extracted from a PDF page based on simple rules.
    """
    logger.debug("Cleaning page text")
    # Normalize newlines and spaces
    text = text.replace("\r\n", "\n")
    text = text.replace("\xa0", " ")

    # Remove extra whitespace
    lines = [line.strip() for line in text.split("\n")]

    # Split into paragraphs
    paragraphs = []
    current_paragraph = []
    for line in lines:
        if line == "":
            # Empty line indicates end of paragraph
            if current_paragraph:
                # Join all lines in the paragraph into a single line
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []
        else:
            # Non-empty line -> part of the current paragraph
            current_paragraph.append(line)

    # Add last paragraph
    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    logger.debug("Cleaned page text")
    # Join paragraphs with a blank line between them
    return "\n\n".join(paragraphs)


def extract_and_clean_pdf(pdf_path: str) -> list[tuple[int, str]]:
    """
    Extracts and cleans text from a PDF and returns a list of tuples containing the page number and the cleaned text on that page.
    """
    pages = extract_text_from_pdf(pdf_path)
    cleaned_pages = [(page_number, clean_page_text(page_text)) for page_number, page_text in pages]

    return cleaned_pages


def pdf_to_full_text(pdf_path: str) -> str:
    """
    Combines pages into one long text with page markers.
    """
    extracted_pages = extract_and_clean_pdf(pdf_path)

    company = os.path.basename(pdf_path).split("_")[0].lower()
    year = os.path.basename(pdf_path).split("_")[1]

    full_text = []
    for page_number, page_text in extracted_pages:
        full_text.append(f"Page {page_number}: {page_text}")

    return {
        "full_text": "\n".join(full_text),
        "metadata": {"source": pdf_path, "company": company, "year": year},
    }
