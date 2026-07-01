"""
image_service.py
-----------------
Handles all communication with the Pollinations image generation API.
Kept separate from app.py so the generation logic can be reused, tested,
or swapped out (e.g. for a different provider) without touching Flask routes.
"""

import os
import random
import requests
from urllib.parse import quote
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

API_URL = "https://image.pollinations.ai/prompt/"

# Preset dimensions per aspect ratio, keyed by (ratio, resolution_scale)
_BASE_DIM = {"standard": 768, "high": 1024}

_RATIOS = {
    "1:1": lambda d: (d, d),
    "16:9": lambda d: (d, int(d * 9 / 16)),
    "9:16": lambda d: (int(d * 9 / 16), d),
    "4:3": lambda d: (d, int(d * 3 / 4)),
}

# Models supported by Pollinations' /prompt endpoint (subset commonly used)
SUPPORTED_MODELS = ["flux", "flux-realism", "flux-anime", "flux-3d", "turbo"]


class ImageGenerationError(Exception):
    """Raised when the image cannot be generated or fails validation."""


def resolve_dimensions(aspect_ratio: str, resolution_scale: str) -> tuple[int, int]:
    """Map UI-friendly aspect ratio + resolution scale to pixel dimensions."""
    base_dim = _BASE_DIM.get(resolution_scale, 768)
    ratio_fn = _RATIOS.get(aspect_ratio, _RATIOS["1:1"])
    return ratio_fn(base_dim)


def build_session() -> requests.Session:
    """Create a requests session with retry/backoff for transient errors."""
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def generate_image(
    prompt: str,
    aspect_ratio: str = "1:1",
    resolution_scale: str = "standard",
    seed: int = -1,
    model: str = "flux",
    enhance: bool = False,
    nologo: bool = True,
    private: bool = True,
) -> bytes:
    """
    Request an image from the Pollinations API and return the raw PNG bytes.

    Raises:
        ImageGenerationError: on network failure, bad response, or invalid payload.
    """
    if not prompt or not prompt.strip():
        raise ImageGenerationError("Prompt cannot be empty.")

    width, height = resolve_dimensions(aspect_ratio, resolution_scale)
    chosen_seed = seed if seed != -1 else random.randint(1, 99_999_999)

    params = {
        "width": width,
        "height": height,
        "seed": chosen_seed,
        "model": model if model in SUPPORTED_MODELS else "flux",
        "nologo": str(nologo).lower(),
        "private": str(private).lower(),
        "enhance": str(enhance).lower(),
    }
    url = f"{API_URL}{quote(prompt)}"

    session = build_session()
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "image/png,image/*;q=0.8"}

    try:
        response = session.get(url, params=params, headers=headers, stream=True, timeout=(5.0, 60))
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise ImageGenerationError(f"Connection failed: {exc}") from exc
    except requests.exceptions.Timeout as exc:
        raise ImageGenerationError("Request timed out.") from exc
    except requests.exceptions.HTTPError as exc:
        raise ImageGenerationError(f"API returned an error: {exc}") from exc

    data = response.content
    if len(data) < 1000:
        raise ImageGenerationError("Response too small — endpoint likely returned an error page.")

    return data