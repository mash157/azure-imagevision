import os
import base64
import io
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from PIL import Image, ImageDraw

# Load environment variables
load_dotenv()

# ✅ Explicit static + template folders for production
app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_vision_client():
    ai_endpoint = os.getenv('AI_ENDPOINT')
    ai_key = os.getenv('AI_KEY')

    if not ai_endpoint or not ai_key:
        raise ValueError("Azure environment variables not set on Render.")

    return ImageAnalysisClient(
        endpoint=ai_endpoint,
        credential=AzureKeyCredential(ai_key)
    )


def draw_bounding_boxes(image, items, mode="objects"):
    draw = ImageDraw.Draw(image)

    for item in items:
        r = item.bounding_box
        box = [r.x, r.y, r.x + r.width, r.y + r.height]

        if mode == "objects":
            draw.rectangle(box, outline="cyan", width=3)
            label = item.tags[0].name if item.tags else "Object"
            draw.text((r.x, r.y), label, fill="cyan")

        elif mode == "people":
            draw.rectangle(box, outline="magenta", width=3)
            draw.text((r.x, r.y), "Person", fill="magenta")

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()


@app.route("/")
def index():
    return render_template("index.html")


# ✅ Health check route (important for Render debugging)
@app.route("/health")
def health():
    return "App is running"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        image_data = file.read()

        client = get_vision_client()

        # ✅ Add safety timeout handling
        result = client.analyze(
            image_data=image_data,
            visual_features=[
                VisualFeatures.CAPTION,
                VisualFeatures.DENSE_CAPTIONS,
                VisualFeatures.TAGS,
                VisualFeatures.OBJECTS,
                VisualFeatures.PEOPLE,
            ]
        )

        response = {
            "caption": result.caption.text if result.caption else "No caption",
            "captionConfidence": round(result.caption.confidence * 100, 1) if result.caption else 0,
            "denseCaptions": [],
            "tags": [],
            "objects": [],
            "objectCount": 0,
            "peopleCount": 0,
            "annotatedImage": None,
            "annotatedPeopleImage": None
        }

        if result.dense_captions:
            response["denseCaptions"] = [
                {"text": c.text, "confidence": round(c.confidence * 100, 1)}
                for c in result.dense_captions.list
            ]

        if result.tags:
            response["tags"] = [
                {"name": t.name, "confidence": round(t.confidence * 100, 1)}
                for t in result.tags.list
            ]

        if result.objects:
            response["objectCount"] = len(result.objects.list)

            response["objects"] = [
                {
                    "name": o.tags[0].name if o.tags else "Unknown",
                    "confidence": round(o.tags[0].confidence * 100, 1) if o.tags else 0
                }
                for o in result.objects.list
            ]

            image = Image.open(io.BytesIO(image_data))
            response["annotatedImage"] = draw_bounding_boxes(image, result.objects.list)

        if result.people:
            response["peopleCount"] = len(result.people.list)

            image = Image.open(io.BytesIO(image_data))
            response["annotatedPeopleImage"] = draw_bounding_boxes(
                image, result.people.list, "people"
            )

        return jsonify(response)

    except Exception as e:
        print("Analyze Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large (max 16MB)'}), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)