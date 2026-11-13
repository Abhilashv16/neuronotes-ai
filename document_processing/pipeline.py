
from pathlib import Path

from document_processing.pdf_extractor import extract_pdf_text
from document_processing.ocr_engine import extract_image_text


def process_document(file_path):
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        result = extract_pdf_text(file_path)

        pages = result["pages"]
        ocr_used = False

        # Use OCR on pages with little or no embedded text.
        import fitz
        from PIL import Image
        import pytesseract
        from document_processing.image_processor import preprocess_image
        import cv2
        import numpy as np

        with fitz.open(file_path) as pdf:
            for index, page in enumerate(pdf):
                if len(pages[index]["text"]) < 20:
                    pixmap = page.get_pixmap(
                        matrix=fitz.Matrix(2, 2),
                        alpha=False
                    )

                    image = Image.frombytes(
                        "RGB",
                        [pixmap.width, pixmap.height],
                        pixmap.samples
                    )

                    gray = cv2.cvtColor(
                        np.array(image),
                        cv2.COLOR_RGB2GRAY
                    )

                    height, width = gray.shape
                    if max(height, width) < 1800:
                        scale = 1800 / max(height, width)
                        gray = cv2.resize(
                            gray, None,
                            fx=scale, fy=scale,
                            interpolation=cv2.INTER_CUBIC
                        )

                    processed = cv2.adaptiveThreshold(
                        gray, 255,
                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY, 31, 11
                    )

                    pages[index]["text"] = pytesseract.image_to_string(
                        processed,
                        config="--oem 3 --psm 6"
                    ).strip()

                    ocr_used = True

        result["text"] = "\n\n".join(
            page["text"] for page in pages
        )
        result["ocr_used"] = ocr_used

        return result

    elif extension in [".jpg", ".jpeg", ".png"]:
        text = extract_image_text(file_path)

        return {
            "page_count": 1,
            "pages": [{"page": 1, "text": text}],
            "text": text,
            "ocr_used": True
        }

    else:
        raise ValueError("Unsupported document format")
