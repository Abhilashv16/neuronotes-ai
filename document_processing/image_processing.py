
import cv2


def preprocess_image(image_path):
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError("Unable to read image")

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
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
