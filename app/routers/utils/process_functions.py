from io import BytesIO

import requests
from PIL import Image
from fastapi import HTTPException


def compress_image(image_url: str) -> BytesIO:
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # Compress the image to 50% quality
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=50)
        buffer.seek(0)
        return buffer
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")

