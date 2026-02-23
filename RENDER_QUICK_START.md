# Render.com - Quick Deploy (Copy & Paste)

## 🚀 Deploy in 3 Steps

### Step 1: Push Code to GitHub

```powershell
cd c:\Users\USER\Downloads\mslearn-ai-vision-main\Labfiles\vision-webapp

git init
git add .
git commit -m "Azure AI Vision - ready for deployment"

# Create new public repo on github.com first, then:
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/vision-webapp.git
git push -u origin main
```

### Step 2: Go to Render.com

1. Visit [render.com](https://render.com)
2. Sign up (free)
3. Click **New** → **Web Service**
4. Select your GitHub repo
5. Click **Connect**

### Step 3: Configure & Deploy

Fill in dashboard form:
- **Name:** `azure-ai-vision`
- **Environment:** `Python 3`
- **Build:** `pip install -r requirements.txt`
- **Start:** `gunicorn app:app`

Add environment variables:
```
AI_ENDPOINT = https://imagesaivision.cognitiveservices.azure.com/
AI_KEY=YOUR_AZURE_KEY_HERE
FLASK_ENV = production
```

Click **Create Web Service** ✅

---

## ✅ Done!

Your app is live in ~1-2 minutes:
```
https://azure-ai-vision.onrender.com
```

---

## 📝 Notes

- Free tier has 15-min auto-sleep (first request slow)
- Unlimited free projects
- Auto-deploy on git push
- HTTPS included
- 750 hours/month free

---

## 🔄 Update App

Just push to GitHub, Render auto-deploys:
```powershell
git add .
git commit -m "Update"
git push
```

---

**That's it! You're live! 🎉**
