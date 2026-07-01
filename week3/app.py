"""
app.py
------
Flask backend exposing a single JSON API for image generation, plus the
page that hosts the frontend form. Keeps HTTP concerns separate from the
generation logic in image_service.py.
"""

import base64
from flask import Flask, render_template, request, jsonify

from image_service import generate_image, ImageGenerationError, SUPPORTED_MODELS

app = Flask(__name__)


@app.route("/")
def index():
    """Render the studio UI, passing the model list so the dropdown stays in sync."""
    return render_template("index.html", models=SUPPORTED_MODELS)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """
    Accepts generation parameters as JSON and returns the image as a
    base64 data URI so the frontend can render it directly in an <img> tag.
    """
    payload = request.get_json(silent=True) or {}

    try:
        image_bytes = generate_image(
            prompt=payload.get("prompt", ""),
            aspect_ratio=payload.get("aspect_ratio", "1:1"),
            resolution_scale=payload.get("resolution_scale", "standard"),
            seed=int(payload.get("seed", -1)),
            model=payload.get("model", "flux"),
            enhance=bool(payload.get("enhance", False)),
            nologo=bool(payload.get("nologo", True)),
            private=bool(payload.get("private", True)),
        )
    except ImageGenerationError as exc:
        return jsonify({"error": str(exc)}), 400
    except (ValueError, TypeError) as exc:
        return jsonify({"error": f"Invalid parameter: {exc}"}), 400

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return jsonify({"image": f"data:image/png;base64,{encoded}"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)