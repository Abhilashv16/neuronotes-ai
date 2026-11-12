
import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
from PIL import Image
from io import BytesIO


def preprocess_image(image_bytes):
    image = Image.open(
        BytesIO(image_bytes)
    ).convert("RGB")

    image_array = np.array(image)

    gray = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY
    )

    processed = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    processed = cv2.adaptiveThreshold(
        processed,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return processed


def extract_text_from_image(image_bytes):
    processed_image = preprocess_image(image_bytes)

    try:
        text = pytesseract.image_to_string(
            processed_image,
            config="--psm 3"
        )

        return text.strip()

    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(
            "Tesseract OCR is not installed or not available in PATH"
        )
