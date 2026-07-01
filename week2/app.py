"""
app.py
Flask backend for the AI Marketing Copy Generator.

Routes:
    GET  /          -> renders the input form UI
    POST /generate  -> accepts JSON {product_name, description, platform,
                        temperature, top_p}, returns {markdown: str} or
                        {error: str}
"""

from flask import Flask, render_template, request, jsonify
from generator import generate_marketing_copy, PLATFORM_TONES

app = Flask(__name__)


@app.route("/")
def index():
    """Render the form. Platform choices are sourced from generator.py so the
    UI and generation logic never drift out of sync."""
    return render_template("index.html", platforms=list(PLATFORM_TONES.keys()))


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    product_name = (data.get("product_name") or "").strip()
    description = (data.get("description") or "").strip()
    platform = data.get("platform", "")
    temperature = data.get("temperature", 0.7)
    top_p = data.get("top_p", 0.9)

    # --- Validation ----------------------------------------------------
    if not product_name or not description:
        return jsonify({"error": "Product name and description are required."}), 400

    if platform not in PLATFORM_TONES:
        return jsonify({"error": "Please select a valid platform."}), 400

    try:
        temperature = float(temperature)
        top_p = float(top_p)
        if not (0.0 <= temperature <= 2.0):
            raise ValueError("temperature out of range")
        if not (0.0 <= top_p <= 1.0):
            raise ValueError("top_p out of range")
    except (TypeError, ValueError):
        return jsonify(
            {"error": "Temperature must be 0-2 and Top-P must be 0-1."}
        ), 400

    # --- Generation ------------------------------------------------------
    try:
        markdown_text = generate_marketing_copy(
            product_name=product_name,
            description=description,
            platform=platform,
            temperature=temperature,
            top_p=top_p,
        )
        return jsonify({"markdown": markdown_text})
    except Exception as exc:  # noqa: BLE001 - surface API errors to the client
        return jsonify({"error": f"Generation failed: {exc}"}), 502


if __name__ == "__main__":
    app.run(debug=True, port=5000)