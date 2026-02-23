# Azure AI Vision Web Application

A modern, full-stack web application for intelligent image analysis using Azure's Computer Vision API. Features a sleek glassmorphism UI with real-time image analysis capabilities.

## ✨ Features

### Image Analysis Capabilities
- **Caption Generation**: AI-generated descriptions of images
- **Dense Captions**: Multiple detailed descriptions of image regions
- **Tag Recognition**: Automatic tag detection with confidence scores
- **Object Detection**: Identifies objects with bounding boxes and labels
- **People Detection**: Detects and locates people in images with confidence metrics

### User Interface
- 🎨 **Modern Glassmorphism Design**: Soft, elegant UI aesthetic with gradient backgrounds
- 📱 **Fully Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- 🎯 **Drag & Drop Upload**: Intuitive file upload with preview
- ⚡ **Real-time Feedback**: Loading indicators and instant result display
- 🎭 **Smooth Animations**: Professional transitions and hover effects
- 🌈 **Professional Color Palette**: Blue/indigo gradient with subtle shadow effects
- ♿ **Accessible**: Full keyboard navigation and screen reader support

### Technical Highlights
- **Backend**: Flask with Python
- **Frontend**: Bootstrap 5 with custom CSS3
- **API**: REST endpoints with JSON responses
- **Security**: Environment variables for sensitive credentials
- **Error Handling**: Comprehensive error messages and validation

## 📋 Prerequisites

- Python 3.8 or higher
- Azure Computer Vision resource (free or paid tier)
- Azure API Key and Endpoint

### Get Azure Credentials

1. Go to [Azure Portal](https://portal.azure.com/)
2. Create a new resource or use existing Computer Vision resource
3. Copy your API key and endpoint URL
4. Note: Free tier allows 20 API calls per minute

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd vision-webapp
```

### 2. Create Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` and add your Azure credentials:

```
AI_ENDPOINT=https://<your-resource-name>.cognitiveservices.azure.com/
AI_KEY=<your-api-key>
FLASK_ENV=development
FLASK_DEBUG=True
```

**Find your credentials:**
- **Endpoint**: In Azure Portal > Your Computer Vision Resource > Keys and Endpoint
- **API Key**: Same location as endpoint, labeled as "Key 1" or "Key 2"

### 5. Run the Application

```bash
python app.py
```

The application will start at: `http://localhost:5000`

### 6. Access the Web Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 🎯 How to Use

1. **Upload an Image**:
   - Click on the upload zone or drag and drop an image
   - Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP

2. **Analyze**:
   - Click the "Analyze Image" button
   - Wait for the AI model to process

3. **View Results**:
   - **Caption**: AI-generated description with confidence score
   - **Dense Captions**: Multiple region descriptions
   - **Tags**: Recognized concepts and objects
   - **Objects**: Detected items with bounding boxes in cyan
   - **People**: Detected people with bounding boxes in magenta

4. **Analyze Another**:
   - Click "Analyze Another Image" to process a new image

## 📁 Project Structure

```
vision-webapp/
├── app.py                      # Flask application & API endpoints
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Environment variables (create from .env.example)
│
├── templates/
│   └── index.html             # Main web interface
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling (glassmorphism)
│   └── uploads/               # Temporary uploaded files (auto-created)
│
└── README.md                  # This file
```

## 🔧 API Endpoints

### POST /analyze
Analyzes an uploaded image and returns AI Vision results.

**Request:**
```
Content-Type: multipart/form-data
Body: image (file)
```

**Response:**
```json
{
  "caption": "A person sitting at a desk",
  "captionConfidence": 95.5,
  "denseCaptions": [
    {
      "text": "person working on laptop",
      "confidence": 88.3
    }
  ],
  "tags": [
    {
      "name": "computer",
      "confidence": 95.0
    }
  ],
  "objectCount": 3,
  "objects": [
    {
      "name": "laptop",
      "confidence": 92.1,
      "bounds": {
        "x": 100,
        "y": 50,
        "width": 200,
        "height": 150
      }
    }
  ],
  "peopleCount": 1,
  "annotatedImage": "base64_encoded_image_jpeg",
  "annotatedPeopleImage": "base64_encoded_image_jpeg"
}
```

## 🛡️ Security Considerations

- ✅ API credentials stored in `.env` file (never in code)
- ✅ `.env` file should be added to `.gitignore`
- ✅ File size limited to 16MB
- ✅ Input validation for file types
- ✅ No sensitive data exposed in frontend

### .gitignore
```
.env
__pycache__/
venv/
.DS_Store
*.pyc
static/uploads/*
```

## 🎨 Customization

### Change Color Scheme

Edit `static/css/style.css` in the `:root` section:

```css
:root {
    --gradient-start: #667eea;  /* Change primary gradient color */
    --gradient-end: #764ba2;    /* Change secondary gradient color */
}
```

### Modify Font

Update the Google Fonts link in `templates/index.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=YOUR_FONT:wght@300;400;600;700&display=swap" rel="stylesheet">
```

### Adjust Layout

Modify `glass-card` padding in CSS:

```css
.glass-card {
    padding: 3rem;  /* Adjust spacing */
}
```

## 🐛 Troubleshooting

### Issue: "AI_ENDPOINT and AI_KEY must be set in .env file"
**Solution**: 
- Ensure `.env` file exists in the project root
- Verify environment variables are correctly set
- Restart the Flask application

### Issue: 403 Unauthorized Error
**Solution**:
- Check that your API key is correct
- Verify your endpoint URL is properly formatted
- Ensure your Azure resource is active

### Issue: Image Too Large
**Solution**:
- Maximum file size is 16MB
- Compress or resize your image
- Use acceptable formats: PNG, JPG, GIF, BMP, WEBP

### Issue: Port 5000 Already in Use
**Solution**:
```bash
# Change port in app.py
# Change line: app.run(debug=True, host='0.0.0.0', port=5000)
# To: app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Module Not Found
**Solution**:
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 📊 Supported Image Features

| Feature | Detection | Accuracy |
|---------|-----------|----------|
| Caption | Single comprehensive description | ~95% |
| Dense Captions | Multiple region descriptions | ~90% |
| Tags | Concept recognition | ~92% |
| Objects | Item detection & localization | ~88% |
| People | Human detection & localization | ~94% |

## 📝 Configuration Options

### Flask Configuration
Edit `app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size
```

### Allowed File Types
In `app.py`:

```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
```

## 🚀 Deployment

### Deploy to Azure App Service

1. Create an Azure App Service
2. Set environment variables in App Service configuration
3. Deploy using Git or ZIP upload
4. Ensure Python 3.8+ runtime is selected

### Deploy to Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn app:app
```

3. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

## 📚 Azure Vision API Documentation

- [Azure Computer Vision Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/)
- [Python SDK Reference](https://learn.microsoft.com/en-us/python/api/azure-ai-vision-imageanalysis/)
- [API Capabilities](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/overview-vision)

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| python-dotenv | 1.0.0 | Environment configuration |
| azure-ai-vision-imageanalysis | 1.0.0b1 | Azure Computer Vision API |
| Pillow | 10.1.0 | Image processing |
| Werkzeug | 3.0.1 | WSGI utilities |

## 💡 Tips & Tricks

1. **Batch Processing**: Modify the backend to process multiple images
2. **Custom Models**: Integrate Custom Vision for specialized detection
3. **Result Export**: Add CSV/JSON export functionality
4. **Image History**: Implement SQLite database to store analysis history
5. **Performance**: Use async processing for faster responses

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve this application!

## ❓ FAQ

**Q: Can I use the free tier of Azure Computer Vision?**
A: Yes! The free tier includes 20 API calls per minute, perfect for testing.

**Q: What's the maximum file size?**
A: Currently set to 16MB. You can modify this in `app.py`.

**Q: Can I run this on my local machine?**
A: Yes! Just ensure you have Python installed and Azure credentials configured.

**Q: How do I change the UI colors?**
A: Edit the CSS variables in `static/css/style.css` under `:root`.

**Q: Is my image data secure?**
A: Images are sent to Azure for analysis. Azure stores them briefly. Refer to [Azure Privacy Policy](https://privacy.microsoft.com/en-us/privacystatement).

---

**Happy Image Analyzing! 🎉**

For support, visit the [Azure Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/) or [Flask Documentation](https://flask.palletsprojects.com/).
