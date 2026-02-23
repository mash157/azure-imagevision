# 🚀 Quick Setup Guide for Windows

## Step-by-Step Installation (Windows)

### Step 1: Prerequisites Check
- ✅ Python 3.8+ installed
- ✅ Azure Computer Vision resource created
- ✅ API Key and Endpoint ready

### Step 2: Clone or Navigate to Project

```powershell
cd vision-webapp
```

### Step 3: Create Virtual Environment

In PowerShell or Command Prompt:

```powershell
python -m venv venv
```

### Step 4: Activate Virtual Environment

**PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

✅ You should see `(venv)` at the beginning of your terminal prompt.

### Step 5: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will take 1-2 minutes. You'll see packages being installed.

### Step 6: Create .env File

**PowerShell:**
```powershell
Copy-Item .env.example .env
```

**Or manually:**
1. Open `.env.example` in your text editor
2. Save it as `.env` in the same folder

### Step 7: Configure Azure Credentials

1. Open `.env` with your text editor
2. Replace placeholder values:

```
AI_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AI_KEY=your-actual-api-key
FLASK_ENV=development
FLASK_DEBUG=True
```

**Where to find these:**
- Go to [Azure Portal](https://portal.azure.com/)
- Select your Computer Vision resource
- Click "Keys and Endpoint" in the left menu
- Copy Endpoint URL and Key 1

### Step 8: Run the Application

With virtual environment activated:

```powershell
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 9: Open in Browser

1. Go to: `http://localhost:5000`
2. Upload an image
3. Click "Analyze Image"
4. See results!

## 🎉 You're All Set!

## Common Errors & Solutions

### Error: "No module named 'flask'"
```powershell
# Make sure virtual environment is activated
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "AI_ENDPOINT and AI_KEY must be set"
- Check `.env` file exists in project root
- No spaces around `=` sign
- Restart Flask (`Ctrl+C` then `python app.py`)

### Error: "Port 5000 already in use"
```powershell
# Use different port
python app.py  # in app.py, change port=5000 to port=5001
```

### Error: "SSL Certificate Verify Failed"
```powershell
pip install --upgrade certifi
```

## ✨ Features Included

- ✅ Modern glassmorphism UI design
- ✅ Drag & drop image upload
- ✅ Real-time image analysis
- ✅ Object detection with bounding boxes
- ✅ People detection and localization
- ✅ Caption generation
- ✅ Tag recognition
- ✅ Fully responsive design
- ✅ Mobile-friendly interface

## 📱 Test on Different Devices

**Mobile Testing:**
1. Get your computer's IP: `ipconfig` (look for IPv4 Address)
2. On mobile, go to: `http://<your-ip>:5000`

## 💾 Useful Commands

```powershell
# Deactivate virtual environment
deactivate

# Reactivate later
venv\Scripts\Activate.ps1

# Freeze dependencies
pip freeze > requirements.txt

# Check installed packages
pip list
```

## 🔒 Security Reminder

⚠️ **IMPORTANT:**
- Never commit `.env` file to Git
- `.gitignore` already configured to exclude it
- Use different API keys for production
- Rotate API keys periodically

## 📊 Performance Tips

1. **Compress images** before uploading for faster analysis
2. **Azure Free Tier**: 20 API calls per minute
3. **Standard Tier**: Up to 10 API calls per second

## 🆘 Still Having Issues?

1. Check Python version: `python --version` (should be 3.8+)
2. Verify Azure resource is active in portal
3. Test API credentials with a simple script
4. Check firewall isn't blocking localhost:5000

## 📚 Next Steps

- Customize colors in `static/css/style.css`
- Add more features (image history, batch processing)
- Deploy to Azure App Service
- Integrate with your application

---

**Happy Analyzing! 🎉**
