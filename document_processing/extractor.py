
from pathlib import Path
import fitz

from document_processing.ocr import extract_text_from_image


def extract_pdf_text(file_path):
    document = fitz.open(file_path)

    extracted_pages = []

    try:
        for page in document:
            text = page.get_text("text")
            extracted_pages.append(text)

        combined_text = "\n".join(extracted_pages)

        # Use OCR for scanned PDFs with little extractable text
        if len(combined_text.strip()) < 80:
            ocr_pages = []

            for page in document:
                pixmap = page.get_pixmap(
                    dpi=200,
                    alpha=False
                )

                image_bytes = pixmap.tobytes("png")

                text = extract_text_from_image(
                    image_bytes
                )

                ocr_pages.append(text)

            combined_text = "\n".join(ocr_pages)

        return combined_text.strip()

    finally:
        document.close()


def extract_document_text(file_path):
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension in {".jpg", ".jpeg", ".png"}:
        with open(file_path, "rb") as file:
            return extract_text_from_image(file.read())

    raise ValueError("Unsupported document format")
