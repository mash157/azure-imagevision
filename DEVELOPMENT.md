# Development Guide

## Project Architecture

### Frontend Architecture
```
templates/index.html
├── HTML Structure
│   ├── Header section with branding
│   ├── Upload area (drag & drop)
│   ├── Preview container
│   ├── Results section (dynamic)
│   └── Error handling
│
└── JavaScript
    ├── File upload handlers
    ├── Drag & drop logic
    ├── API communication (fetch)
    ├── Results rendering
    └── Error display
```

### Backend Architecture
```
app.py
├── Flask Setup
├── Configuration & Security
├── Azure Vision Client
└── API Endpoints
    ├── GET / (serve index.html)
    └── POST /analyze
        ├── File validation
        ├── Azure API call
        ├── Image processing
        ├── Results formatting
        └── JSON response
```

## Key Components

### 1. Flask App Configuration
```python
app.config['MAX_CONTENT_LENGTH']  # File size limit
app.config['UPLOAD_FOLDER']       # Uploads directory
ALLOWED_EXTENSIONS                # File type whitelist
```

### 2. Azure Vision Integration
- Uses `azure-ai-vision-imageanalysis` SDK
- Analyzes: Caption, Dense Captions, Tags, Objects, People
- Credentials from `.env` file

### 3. Image Processing
- PIL/Pillow for bounding box drawing
- Base64 encoding for image transmission
- Cyan boxes for objects, magenta for people

### 4. Frontend UI Framework
- Bootstrap 5 for responsiveness
- Custom CSS for glassmorphism effect
- JavaScript for interactivity

## Adding New Features

### Add New Analysis Feature

1. **Backend (app.py)**:
```python
# Add to analyze endpoint
from azure.ai.vision.imageanalysis.models import VisualFeatures

# In analyze() function:
result = cv_client.analyze(
    image_data=image_data,
    visual_features=[
        VisualFeatures.SMART_CROPS,  # NEW FEATURE
    ],
)
```

2. **Response (app.py)**:
```python
response_data['smartCrops'] = [...]
```

3. **Frontend (templates/index.html)**:
```javascript
// In displayResults() function
if (data.smartCrops && data.smartCrops.length > 0) {
    document.getElementById('smartCropsSection').classList.remove('d-none');
    // Render results
}
```

### Add Database Storage

```python
# Install Flask-SQLAlchemy
pip install Flask-SQLAlchemy

# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    caption = db.Column(db.String(500))
    tags = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.now)
```

### Add Export Functionality

```python
from flask import send_file
import json

@app.route('/export/<int:result_id>')
def export_results(result_id):
    result = AnalysisResult.query.get(result_id)
    data = {
        'caption': result.caption,
        'tags': result.tags,
        # ... more fields
    }
    return jsonify(data)
```

### Improve Performance

```python
# Use async processing
from celery import Celery

celery = Celery(app.name)

@celery.task
def analyze_image_async(image_path):
    # Long-running analysis
    pass
```

## Testing

### Manual Testing

1. **Valid Image Test**:
   - Upload PNG, JPG, GIF
   - Verify all features detected

2. **Edge Cases**:
   - Very large image (>16MB)
   - Invalid format
   - Corrupted file

3. **UI Testing**:
   - Mobile responsiveness
   - Drag & drop functionality
   - Error messages display

### Unit Testing

```python
# test_app.py
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_index(self):
        response = self.app.get('/')
        assert response.status_code == 200
    
    def test_analyze_no_file(self):
        response = self.app.post('/analyze')
        assert response.status_code == 400
```

## Performance Optimization

### Caching Results
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/analyze', methods=['POST'])
@cache.cached(timeout=3600)
def analyze():
    # Results cached for 1 hour
```

### Image Compression
```python
from PIL import Image

def compress_image(image, quality=85):
    image.thumbnail((1920, 1080))
    return image
```

### Database Optimization
```python
# Index frequently queried columns
class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)
```

## Security Enhancements

### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze():
    pass
```

### CORS Configuration
```python
from flask_cors import CORS

CORS(app, resources={r"/api/*": {"origins": ["yourdomain.com"]}})
```

### Input Validation
```python
from werkzeug.utils import secure_filename

def validate_file(file):
    if not file or file.filename == '':
        return False
    
    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        return False
    
    return True
```

## Deployment Checklist

- [ ] Remove `FLASK_DEBUG=True` from production `.env`
- [ ] Use production WSGI server (Gunicorn)
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Test with production Azure key
- [ ] Set up monitoring
- [ ] Configure firewall rules
- [ ] Set up CI/CD pipeline

## Useful Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Azure Computer Vision API](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Python Pillow Docs](https://pillow.readthedocs.io/)

## Common Issues & Solutions

### Issue: Image Analysis is Slow
- Azure free tier has rate limits (20/min)
- Use Standard tier for production
- Implement caching for duplicate images

### Issue: Bounding Boxes Not Showing
- Check image format (supports JPEG, PNG, GIF)
- Verify coordinates are within image bounds
- Test with different image sizes

### Issue: Memory Issues with Large Files
- Compress images on upload
- Implement streaming for large files
- Use asynchronous processing

## Future Enhancement Ideas

1. **Batch Processing**: Analyze multiple images
2. **Custom Vision Models**: Train on specific datasets
3. **Image History**: Store and retrieve past analyses
4. **Export Options**: PDF, CSV, JSON reports
5. **Real-time Webcam**: Analyze webcam feed
6. **Mobile App**: React Native or Flutter app
7. **Team Collaboration**: Share results with others
8. **Analytics Dashboard**: Usage statistics
9. **API Rate Dashboard**: Monitor API usage
10. **Scheduled Analysis**: Process images on schedule

---

Happy Developing! 🚀
