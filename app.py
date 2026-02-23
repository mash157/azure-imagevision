import os
import base64
import io
import traceback
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from PIL import Image, ImageDraw

# Load environment variables
load_dotenv()

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}


# ------------------------------------------------
# Utility Functions
# ------------------------------------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_vision_client():
    endpoint = os.getenv("AI_ENDPOINT")
    key = os.getenv("AI_KEY")

    if not endpoint or not key:
        raise ValueError("Azure environment variables not set.")

    return ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )


def draw_bounding_boxes(image_data, items, mode="objects"):
    """
    Memory-safe image processing.
    Opens image inside context manager and auto closes.
    """

    with Image.open(io.BytesIO(image_data)) as image:

        # Ensure no RGBA crash
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        draw = ImageDraw.Draw(image)

        for item in items:
            r = item.bounding_box
            box = [r.x, r.y, r.x + r.width, r.y + r.height]

            if mode == "objects":
                draw.rectangle(box, outline="cyan", width=3)

            elif mode == "people":
                draw.rectangle(box, outline="magenta", width=3)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode()


# ------------------------------------------------
# Routes
# ------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return "App is running"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        image_data = file.read()

        client = get_vision_client()

        result = client.analyze(
            image_data=image_data,
            visual_features=[
                VisualFeatures.CAPTION,
                VisualFeatures.DENSE_CAPTIONS,
                VisualFeatures.TAGS,
                VisualFeatures.OBJECTS,
                VisualFeatures.PEOPLE,
            ],
        )

        response = {
            "caption": result.caption.text if result.caption else "No caption",
            "captionConfidence": round(result.caption.confidence * 100, 1)
            if result.caption else 0,
            "denseCaptions": [],
            "tags": [],
            "objects": [],
            "objectCount": 0,
            "peopleCount": 0,
            "annotatedImage": None,
            "annotatedPeopleImage": None,
        }

        # Dense captions
        if result.dense_captions:
            response["denseCaptions"] = [
                {
                    "text": c.text,
                    "confidence": round(c.confidence * 100, 1),
                }
                for c in result.dense_captions.list
            ]

        # Tags
        if result.tags:
            response["tags"] = [
                {
                    "name": t.name,
                    "confidence": round(t.confidence * 100, 1),
                }
                for t in result.tags.list
            ]

        # Objects
        if result.objects:
            response["objectCount"] = len(result.objects.list)

            response["objects"] = [
                {
                    "name": o.tags[0].name if o.tags else "Unknown",
                    "confidence": round(o.tags[0].confidence * 100, 1)
                    if o.tags else 0,
                }
                for o in result.objects.list
            ]

            response["annotatedImage"] = draw_bounding_boxes(
                image_data, result.objects.list, "objects"
            )

        # People
        if result.people:
            response["peopleCount"] = len(result.people.list)

            response["annotatedPeopleImage"] = draw_bounding_boxes(
                image_data, result.people.list, "people"
            )

        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large (max 16MB)"}), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)