
from pathlib import Path

import fitz
import cv2
import numpy as np
import pytesseract

from PIL import Image


def preprocess_image(image):
    image_array = np.array(image.convert("RGB"))

    gray = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY
    )

    height, width = gray.shape

    if max(height, width) < 1800:
        scale = 1800 / max(height, width)

        gray = cv2.resize(
            gray,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC
        )

    denoised = cv2.medianBlur(gray, 3)

    processed = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return processed


def extract_image_text(image):
    processed = preprocess_image(image)

    try:
        return pytesseract.image_to_string(
            processed,
            config="--oem 3 --psm 6"
        ).strip()

    except pytesseract.TesseractNotFoundError as error:
        raise RuntimeError(
            "Tesseract OCR is not installed or configured."
        ) from error


def extract_document_text(file_path):
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":

        extracted_pages = []

        try:
            with fitz.open(file_path) as pdf:

                for page in pdf:
                    text = page.get_text("text").strip()

                    # OCR scanned pages
                    if len(text) < 20:

                        pix = page.get_pixmap(
                            matrix=fitz.Matrix(2, 2),
                            alpha=False
                        )

                        image = Image.frombytes(
                            "RGB",
                            [pix.width, pix.height],
                            pix.samples
                        )

                        text = extract_image_text(image)

                    extracted_pages.append(text)

            return "\n\n".join(extracted_pages).strip()

        except RuntimeError:
            raise

        except Exception as error:
            raise RuntimeError(
                f"PDF extraction failed: {error}"
            ) from error

    elif extension in [".jpg", ".jpeg", ".png"]:

        try:
            with Image.open(file_path) as image:
                return extract_image_text(image)

        except RuntimeError:
            raise

        except Exception as error:
            raise RuntimeError(
                f"Image extraction failed: {error}"
            ) from error

    else:
        raise ValueError("Unsupported document format")
