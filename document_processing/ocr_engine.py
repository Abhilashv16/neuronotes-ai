
import pytesseract

from PIL import Image
from document_processing.image_processor import preprocess_image


def extract_image_text(image_path):
    processed_image = preprocess_image(image_path)

    try:
        text = pytesseract.image_to_string(
            processed_image,
            config="--oem 3 --psm 6"
        )

        return text.strip()

    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(
            "Tesseract OCR is not installed or not configured."
        )
