from barcode import EAN13, EAN8, Code39
from barcode.errors import BarcodeError
import os
import logging

logger = logging.getLogger(__name__)

# Configuration
BARCODE_DIR = "static/images/temp_ucp"


def make_barcode(code):
    """
    Generate a barcode from the given code.

    Args:
        code: The code to encode in the barcode

    Returns:
        str: Path to the generated barcode file (without extension)

    Raises:
        ValueError: If the code is invalid
        BarcodeError: If barcode generation fails
    """
    if not code:
        raise ValueError("Code cannot be empty")

    number = str(code).strip()

    # Validate input
    if not number.isdigit():
        logger.warning(f"Non-numeric code provided: {code}")
    if len(number) > 50:
        raise ValueError("Code is too long (max 50 characters)")

    # Select barcode type based on code length
    try:
        if len(number) == 13:
            my_code = EAN13(number)
        elif len(number) == 8:
            my_code = EAN8(number)
        else:
            my_code = Code39(number, add_checksum=False)
    except BarcodeError as e:
        logger.error(f"Barcode creation error: {e}")
        raise ValueError(f"Invalid barcode format: {e}")

    # Ensure directory exists
    os.makedirs(BARCODE_DIR, exist_ok=True)

    # Sanitize filename
    safe_code = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in number)
    path = os.path.join(BARCODE_DIR, safe_code)

    try:
        my_code.save(path)
        logger.info(f"Barcode generated successfully: {path}")
        return path
    except Exception as e:
        logger.error(f"Error saving barcode: {e}")
        raise
