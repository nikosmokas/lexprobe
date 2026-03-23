# Railway Deployment Example
# Railway automatically detects docker-compose.yml and deploys all services

# Prerequisites:
# 1. Create Railway account
# 2. Connect GitHub repository
# 3. Add environment variables in Railway dashboard:
#    - GEMINI_API_KEY
# 4. Railway will auto-deploy on push to main

# No additional workflow needed - Railway handles deployment automatically
# Just push to main and Railway will build and deploy using docker-compose.yml

# railway.json (optional - for custom config)
{
  "build": {
    "builder": "dockerfile",
    "buildCommand": "docker-compose build"
  },
  "deploy": {
    "startCommand": "docker-compose up"
  }
}