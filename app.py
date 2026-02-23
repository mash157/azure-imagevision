import os
import sys
import base64
import io
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from PIL import Image, ImageDraw
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_vision_client():
    """Initialize and return Azure AI Vision client"""
    ai_endpoint = os.getenv('AI_ENDPOINT')
    ai_key = os.getenv('AI_KEY')
    
    if not ai_endpoint or not ai_key:
        raise ValueError("AI_ENDPOINT and AI_KEY must be set in .env file")
    
    return ImageAnalysisClient(
        endpoint=ai_endpoint,
        credential=AzureKeyCredential(ai_key)
    )

def draw_bounding_boxes(image, objects_list, output_type='objects'):
    """Draw bounding boxes on image and return as base64"""
    try:
        draw = ImageDraw.Draw(image)
        
        if output_type == 'objects':
            for detected_object in objects_list:
                r = detected_object.bounding_box
                bounding_box = [
                    r.x,
                    r.y,
                    r.x + r.width,
                    r.y + r.height
                ]
                # Draw rectangle with cyan outline
                draw.rectangle(bounding_box, outline='cyan', width=3)
                # Draw label background
                label = detected_object.tags[0].name if detected_object.tags else "Object"
                bbox_text = draw.textbbox((r.x, r.y), label)
                draw.rectangle(bbox_text, fill='cyan')
                draw.text((r.x, r.y), label, fill='black')
        
        elif output_type == 'people':
            for person in objects_list:
                r = person.bounding_box
                bounding_box = [
                    r.x,
                    r.y,
                    r.x + r.width,
                    r.y + r.height
                ]
                # Draw rectangle with magenta outline
                draw.rectangle(bounding_box, outline='magenta', width=3)
                # Draw label
                confidence = f"{person.confidence * 100:.0f}%"
                bbox_text = draw.textbbox((r.x, r.y), "Person")
                draw.rectangle(bbox_text, fill='magenta')
                draw.text((r.x, r.y), "Person", fill='white')
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    except Exception as e:
        print(f"Error drawing bounding boxes: {e}")
        return None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded image"""
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400
        
        # Read image data
        image_data = file.read()
        file.seek(0)  # Reset file pointer
        
        # Initialize Azure client
        client = get_vision_client()
        
        # Analyze image
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
        
        # Prepare response data
        response_data = {
            'caption': 'No caption available',
            'captionConfidence': 0,
            'denseCaptions': [],
            'tags': [],
            'objects': [],
            'objectCount': 0,
            'peopleCount': 0,
            'annotatedImage': None,
            'annotatedPeopleImage': None
        }
        
        # Extract caption
        if result.caption:
            response_data['caption'] = result.caption.text
            response_data['captionConfidence'] = round(result.caption.confidence * 100, 1)
        
        # Extract dense captions
        if result.dense_captions:
            response_data['denseCaptions'] = [
                {
                    'text': caption.text,
                    'confidence': round(caption.confidence * 100, 1)
                }
                for caption in result.dense_captions.list
            ]
        
        # Extract tags
        if result.tags:
            response_data['tags'] = [
                {
                    'name': tag.name,
                    'confidence': round(tag.confidence * 100, 1)
                }
                for tag in result.tags.list
            ]
        
        # Process objects with bounding boxes
        if result.objects:
            response_data['objectCount'] = len(result.objects.list)
            response_data['objects'] = [
                {
                    'name': obj.tags[0].name if obj.tags else 'Unknown',
                    'confidence': round(obj.tags[0].confidence * 100, 1) if obj.tags else 0,
                    'bounds': {
                        'x': obj.bounding_box.x,
                        'y': obj.bounding_box.y,
                        'width': obj.bounding_box.width,
                        'height': obj.bounding_box.height
                    }
                }
                for obj in result.objects.list
            ]
            
            # Draw bounding boxes for objects
            try:
                image = Image.open(io.BytesIO(image_data))
                annotated_img = draw_bounding_boxes(image, result.objects.list, 'objects')
                response_data['annotatedImage'] = annotated_img
            except Exception as e:
                print(f"Error processing objects image: {e}")
        
        # Process people with bounding boxes
        if result.people:
            response_data['peopleCount'] = len(result.people.list)
            
            # Draw bounding boxes for people
            try:
                image = Image.open(io.BytesIO(image_data))
                annotated_img = draw_bounding_boxes(image, result.people.list, 'people')
                response_data['annotatedPeopleImage'] = annotated_img
            except Exception as e:
                print(f"Error processing people image: {e}")
        
        return jsonify(response_data), 200
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as ex:
        print(f"Error: {ex}")
        return jsonify({'error': f'Analysis failed: {str(ex)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File is too large. Maximum size is 16MB'}), 413

if __name__ == '__main__':
    # For deployment: use PORT env var, for local: default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)