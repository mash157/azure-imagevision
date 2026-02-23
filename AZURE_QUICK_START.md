# Azure Deployment - Quick Reference (Copy & Paste)

## One-Command Setup

Run this in PowerShell (replace app name):

```powershell
# Step 1: Login
az login

# Step 2: Create everything
$rg = "vision-app-rg"
$plan = "vision-app-plan"
$app = "YOUR-UNIQUE-APP-NAME"

az group create --name $rg --location eastus
az appservice plan create --name $plan --resource-group $rg --sku B1 --is-linux
az webapp create --resource-group $rg --plan $plan --name $app --runtime "PYTHON:3.11"

# Step 3: Set environment variables
az webapp config appsettings set --resource-group $rg --name $app --settings `
  AI_ENDPOINT="https://imagesaivision.cognitiveservices.azure.com/" `
  AI_KEY="YOUR-API-KEY-HERE" `
  FLASK_ENV="production"

# Step 4: Deploy
cd c:\Users\USER\Downloads\mslearn-ai-vision-main\Labfiles\vision-webapp
Compress-Archive -Path . -DestinationPath app.zip -Force
az webapp deployment source config-zip --resource-group $rg --name $app --src app.zip

# Done! Your app is at: https://YOUR-UNIQUE-APP-NAME.azurewebsites.net
```

---

## Important Notes

1. **Replace `YOUR-UNIQUE-APP-NAME`** with something unique (e.g., `vision-analyzer-2026`)
2. **Replace API values** with yours from `.env` file
3. **Sku B1** = ~$15/month (recommended for production)
4. **Check deployment logs** if it fails:
   ```powershell
   az webapp log tail --resource-group vision-app-rg --name YOUR-APP-NAME
   ```

---

## What Gets Created

- ✅ Resource Group
- ✅ App Service Plan (B1 tier)
- ✅ Web App with Python 3.11
- ✅ Environment variables configured
- ✅ Your app deployed and running
- ✅ HTTPS enabled automatically

---

## After Deployment

**Your app URL:**
```
https://YOUR-UNIQUE-APP-NAME.azurewebsites.net
```

**Check status:**
```powershell
az webapp show --resource-group vision-app-rg --name YOUR-APP-NAME --query state
```

**View logs:**
```powershell
az webapp log tail --resource-group vision-app-rg --name YOUR-APP-NAME
```

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| App not starting | Check logs: `az webapp log tail...` |
| Environment vars not found | Set again with `az webapp config appsettings set...` |
| 502 Bad Gateway | Wait 2-5 min for cold start, then refresh |
| App name taken | Use different name (must be globally unique) |

---

That's it! 🚀 Go live in 5 minutes!
