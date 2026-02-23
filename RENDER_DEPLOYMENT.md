# Deploy to Render.com - Step by Step

## 🚀 Quick Deploy (3 Minutes)

### Step 1: Prepare Your Code

All files are ready! ✅
- `requirements.txt` ✅
- `render.yaml` ✅
- `app.py` (production-ready) ✅
- `Procfile` ✅

### Step 2: Create GitHub Repository (Easiest)

**Option A: Push to GitHub**

```powershell
# Navigate to project
cd c:\Users\USER\Downloads\mslearn-ai-vision-main\Labfiles\vision-webapp

# Initialize git if not done
git init
git add .
git commit -m "Azure AI Vision webapp - ready for Render deployment"

# Create new repo on GitHub.com, then:
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/vision-webapp.git
git push -u origin main
```

**Option B: Skip GitHub (Direct Upload)**
- You can also deploy directly from ZIP file

---

### Step 3: Sign Up on Render.com

1. Go to [render.com](https://render.com)
2. Click **Sign Up**
3. Use GitHub or email
4. Connect your GitHub account (if using GitHub option)

---

### Step 4: Create New Web Service

1. Click **+ New** → **Web Service**
2. Choose your connection method:

**If using GitHub:**
- Select your `vision-webapp` repository
- Click **Connect**

**If uploading code directly:**
- Choose "Docker" or "Redeploy from previous deploys"
- Upload your project ZIP

---

### Step 5: Configure Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `azure-ai-vision` (or any name) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | `Free` |

---

### Step 6: Add Environment Variables

Click **Advanced** → **Environment Variables**

Add these:
```
AI_ENDPOINT = https://imagesaivision.cognitiveservices.azure.com/
AI_KEY=YOUR_AZURE_KEY_HERE
FLASK_ENV = production
```

---

### Step 7: Deploy!

Click **Create Web Service**

✅ Render will:
1. Build your app (~1-2 minutes)
2. Start the server
3. Give you a live URL!

---

## 🎉 Your Live App!

Your app will be available at:
```
https://azure-ai-vision.onrender.com
```

(Exact URL shown on Render dashboard)

---

## 📊 What Happens on Render

### Free Tier Includes:
✅ 750 free dyno hours/month
✅ Auto-restart if crashes
✅ HTTPS/SSL automatic
✅ Free domain
✅ Persistent storage (512 MB)

### Limitations:
⚠️ Spins down after 15 min inactivity (cold start)
⚠️ Limited to 750 hours/month
⚠️ Shared resources

### To Remove Cold Starts:
- Upgrade to paid plan ($7+/month)
- Or use Render's "Always On" feature

---

## 🔄 Update Your App

### Option 1: Auto-Deploy from GitHub
- Just push to main branch
- Render auto-deploys!

### Option 2: Manual Redeploy
1. Go to Render dashboard
2. Click your service
3. Click **Manual Deploy** → **Deploy latest commit**

---

## 🐛 Troubleshooting

### App shows 502 error?
- Check logs: Dashboard → **Logs**
- Common causes:
  - Missing environment variables
  - Import errors
  - Port not set correctly

### View Logs
1. Go to [render.com/dashboard](https://render.com/dashboard)
2. Click your service name
3. Scroll down to **Logs**

### Check Status
```
https://status.render.com
```

---

## ✅ Deployment Checklist

- [ ] Code ready (all files in vision-webapp folder)
- [ ] `requirements.txt` has gunicorn
- [ ] `render.yaml` created
- [ ] GitHub account ready
- [ ] Code pushed to GitHub
- [ ] Render.com account created
- [ ] Environment variables set
- [ ] Deploy button clicked
- [ ] Wait for build to complete
- [ ] Test the live URL

---

## 🔗 Useful Links

- [Render.com Docs](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Logs & Debugging](https://render.com/docs/troubleshooting)

---

## 💡 Pro Tips

1. **Custom Domain** (optional)
   - Render → Service Settings → Add Custom Domain

2. **Monitor Performance**
   - Dashboard shows CPU, memory usage

3. **Scale Up Later**
   - Can upgrade from Free → Pro anytime

4. **Webhooks** (advanced)
   - Auto-deploys on GitHub push

---

**You're ready! Go to Render.com and deploy! 🚀**

Questions? Check the logs or contact Render support.
