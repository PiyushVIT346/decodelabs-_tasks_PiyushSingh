"""
generator.py
Core logic for AI-powered marketing copy generation using Google Gemini.

Modular by design:
    - PLATFORM_TONES   : default tone/style mapping per platform
    - build_prompt()   : compiles the prompt template
    - generate_marketing_copy() : calls the Gemini API with retry/backoff
"""

import os
import time
from google import genai
from google.genai import types

# --- Client Initialization -------------------------------------------------
# Set your API key as an environment variable before running the app:
#   set GEMINI_API_KEY="your-key-here"
client = genai.Client(api_key="your-key-here")

# Default tone/style applied per platform.
PLATFORM_TONES = {
    "LinkedIn": (
        "Professional, thought-leadership, focused on productivity, "
        "workplace ergonomics, and value delivery"
    ),
    "Instagram": (
        "Trendy, energetic, lifestyle-focused, purely text-based aesthetic"
    ),
    "Email": (
        "Persuasive, direct, benefit-driven, suited for a marketing email "
        "with a clear call-to-action"
    ),
}


def build_prompt(product_name: str, description: str, platform: str, tone: str) -> str:
    """Compile the marketing-copy prompt template for a single generation call."""
    return (
        "You are an expert digital marketer and copywriter.\n"
        "Your task is to transform the following raw product information into "
        "highly engaging copy.\n\n"
        "PRODUCT DETAILS:\n"
        f"- Product Name: {product_name}\n"
        f"- Raw Description: {description}\n\n"
        "TARGET PLATFORM:\n"
        f"{platform}\n\n"
        "REQUIRED TONE:\n"
        f"{tone}\n\n"
        "INSTRUCTIONS:\n"
        f"Write the final marketing copy for {platform}. Embody the {tone} tone "
        "completely. Format the response in clean Markdown (use headings, bold "
        "text, and bullet points where appropriate) so it renders well in a "
        "rich-text viewer. Do not use emojis in the output."
    )


def generate_marketing_copy(
    product_name: str,
    description: str,
    platform: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_retries: int = 3,
) -> str:
    """
    Generate tailored marketing copy for a given platform.

    Retries on transient 503 / 429 (overload / rate-limit) errors using
    exponential backoff (1s, 2s, 4s, ...).

    Raises:
        ValueError: if `platform` is not one of PLATFORM_TONES.
        Exception:  re-raises the original error for non-transient failures,
                    or after retries are exhausted.
    """
    if platform not in PLATFORM_TONES:
        raise ValueError(f"Unsupported platform: {platform}")

    tone = PLATFORM_TONES[platform]
    prompt = build_prompt(product_name, description, platform, tone)
    config = types.GenerateContentConfig(temperature=temperature, top_p=top_p)

    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config,
            )
            return response.text

        except Exception as exc:  # noqa: BLE001 - intentional broad catch for API errors
            last_error = exc
            transient = any(code in str(exc) for code in ("503", "UNAVAILABLE", "429"))
            if transient and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise

    # Unreachable, but keeps type-checkers happy.
    raise last_error  # type: ignore[misc]