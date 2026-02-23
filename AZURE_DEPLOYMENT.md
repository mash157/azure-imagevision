# Deploy to Azure App Service - Complete Guide

## 🚀 Quick Deploy (5 Minutes)

### Prerequisites
- ✅ Azure Account (Free tier or paid)
- ✅ Azure CLI installed
- ✅ Your `.env` file with AI_ENDPOINT and AI_KEY

### Step 1: Login to Azure

Open PowerShell and run:
```powershell
az login
```

This will open a browser to authenticate. After login, you'll see your subscription info.

### Step 2: Create Resource Group

```powershell
$resourceGroup = "vision-app-rg"
$location = "eastus"

az group create --name $resourceGroup --location $location
```

**Result:** You should see `"provisioningState": "Succeeded"`

### Step 3: Create App Service Plan

```powershell
$appServicePlan = "vision-app-plan"
$sku = "B1"  # Free tier: F1, Budget: B1 ($10-15/month)

az appservice plan create `
    --name $appServicePlan `
    --resource-group $resourceGroup `
    --sku $sku `
    --is-linux
```

**Sku Options:**
- `F1` = Free (limited)
- `B1` = Basic ($10-15/month) - RECOMMENDED
- `S1` = Standard ($50+/month)

### Step 4: Create Web App

```powershell
$appName = "vision-analyzer-app"  # Must be globally unique!

az webapp create `
    --resource-group $resourceGroup `
    --plan $appServicePlan `
    --name $appName `
    --runtime "PYTHON:3.11"
```

**Note:** Replace `vision-analyzer-app` with a unique name globally. It will be: `https://vision-analyzer-app.azurewebsites.net`

### Step 5: Configure App Settings (Environment Variables)

```powershell
az webapp config appsettings set `
    --resource-group $resourceGroup `
    --name $appName `
    --settings `
        AI_ENDPOINT="https://imagesaivision.cognitiveservices.azure.com/" `
         AI_KEY=YOUR_AZURE_KEY_HERE
        FLASK_ENV="production" `
        FLASK_DEBUG="False"
```

**Replace with your actual values from `.env`**

### Step 6: Deploy Code via ZIP

**Option A: Deploy from Local Files**

```powershell
# Navigate to project
cd c:\Users\USER\Downloads\mslearn-ai-vision-main\Labfiles\vision-webapp

# Create ZIP archive
Compress-Archive -Path . -DestinationPath app.zip -Force

# Deploy
az webapp deployment source config-zip `
    --resource-group $resourceGroup `
    --name $appName `
    --src app.zip
```

**Option B: Deploy via Git**

```powershell
# Initialize git (if not already)
git init
git add .
git commit -m "Initial deployment"

# Add Azure remote
az webapp deployment source config-local-git `
    --resource-group $resourceGroup `
    --name $appName

# Deploy via git push
git push azure main
```

### Step 7: View Logs

```powershell
# Stream logs
az webapp log tail `
    --resource-group $resourceGroup `
    --name $appName
```

### Your App is Live! 🎉

URL: `https://{appName}.azurewebsites.net`

Example: `https://vision-analyzer-app.azurewebsites.net`

---

## 📊 After Deployment

### Check App Status
```powershell
az webapp show `
    --resource-group $resourceGroup `
    --name $appName `
    --query state
```

### View Logs in Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Search your app name
3. Click "Log stream" to see real-time logs

### Scale Up Later
```powershell
# Upgrade to Standard tier
az appservice plan update `
    --name $appServicePlan `
    --resource-group $resourceGroup `
    --sku S1
```

---

## 🔧 Troubleshooting

### App not starting?
```powershell
# Check deployment logs
az webapp deployment log show `
    --resource-group $resourceGroup `
    --name $appName
```

### Environment variables not loading?
```powershell
# Verify settings were applied
az webapp config appsettings list `
    --resource-group $resourceGroup `
    --name $appName
```

### 502 Bad Gateway?
- Check logs: `az webapp log tail`
- Verify Python runtime is correct
- Make sure PORT environment variable is being used

### Cold Start (slow first request)?
- Normal on free tier
- Upgrade to B1 or higher for faster performance

---

## 💾 Backup Commands (Save These)

### Complete Script for Re-deployment

```powershell
$resourceGroup = "vision-app-rg"
$appServicePlan = "vision-app-plan"
$appName = "vision-analyzer-app"

# Re-deploy latest code
cd c:\Users\USER\Downloads\mslearn-ai-vision-main\Labfiles\vision-webapp
Compress-Archive -Path . -DestinationPath app.zip -Force

az webapp deployment source config-zip `
    --resource-group $resourceGroup `
    --name $appName `
    --src app.zip

# Check status
az webapp show --resource-group $resourceGroup --name $appName --query state
```

### Delete Resource (Clean Up)
```powershell
# WARNING: This deletes everything!
az group delete --name $resourceGroup --yes
```

---

## 🎯 Deployment Checklist

- [ ] Azure CLI installed and logged in
- [ ] `.env` file has correct AI_ENDPOINT and AI_KEY
- [ ] `Procfile` exists in project root
- [ ] `requirements.txt` includes gunicorn
- [ ] `app.py` updated to use PORT env var
- [ ] Unique app name chosen
- [ ] Resource group created
- [ ] App Service Plan created
- [ ] Web App created
- [ ] Environment variables set
- [ ] Code deployed via ZIP or Git
- [ ] App is accessible at azurewebsites.net URL

---

## 📈 Monitor Your App

### View Metrics
```powershell
az monitor metrics list `
    --resource /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Web/sites/{appName} `
    --metric "CpuTime,MemoryPercentage"
```

### Set Up Alerts
In Azure Portal:
1. Go to your app
2. Click "Alerts"
3. Click "Create alert rule"
4. Set conditions (CPU > 80%, Memory > 90%)
5. Add notification email

---

## 🚀 Performance Tips

1. **Enable App Service Always On** (paid tier)
   - Prevents cold starts
   - Available on B1 and higher

2. **Use Compression**
   - Already enabled for gzip on static files

3. **Monitor Quotas** (free tier)
   - 60 min/day CPU time
   - Switch to B1 if hitting limits

4. **Scale Up When Needed**
   ```powershell
   az appservice plan update --sku S1 ...
   ```

---

## 🔐 Security

✅ **Already Configured:**
- HTTPS/SSL (automatic)
- Environment variables protected
- No hardcoded secrets

**Additional Steps (Optional):**
```powershell
# Enable HTTPS only
az webapp update `
    --resource-group $resourceGroup `
    --name $appName `
    --set httpsOnly=true
```

---

## 📞 Need Help?

- [Azure App Service Docs](https://learn.microsoft.com/en-us/azure/app-service/)
- [Python on App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)

---

**Your app will be live in ~5 minutes! 🎉**

Start with Step 1 above.
