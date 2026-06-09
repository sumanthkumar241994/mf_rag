# ingestion/extract_pdf.py

import pymupdf


def extract_pdf_text(pdf_path: str) -> list[dict]:
    """
    Returns:
    [
        {
            "page_number": 1,
            "text": "Investment Objective..."
        },
        {
            "page_number": 2,
            "text": "Asset Allocation..."
        }
    ]
    """

    document = pymupdf.open(pdf_path)

    pages = []

    for page_num in range(len(document)):
        page = document[page_num]

        text = page.get_text("text")

        pages.append(
            {
                "page_number": page_num + 1,
                "text": text.strip()
            }
        )

    document.close()

    return pages