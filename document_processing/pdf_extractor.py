
import fitz


def extract_pdf_text(file_path):
    pages = []

    try:
        with fitz.open(file_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                pages.append({
                    "page": page_number,
                    "text": text
                })

        return {
            "page_count": len(pages),
            "pages": pages,
            "text": "\n\n".join(
                page["text"] for page in pages
            )
        }

    except Exception as error:
        raise RuntimeError(
            f"PDF extraction failed: {error}"
        )
