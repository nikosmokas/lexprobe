#!/bin/bash

# LexProbe Deployment Configurator

echo "🚀 LexProbe Deployment Configurator"
echo "=================================="
echo ""

echo "Choose your deployment platform:"
echo "1) Railway (Easiest - auto-deploys from GitHub)"
echo "2) VPS (DigitalOcean/Linode/AWS EC2)"
echo "3) Local development only"
echo ""

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📋 Railway Deployment Setup:"
        echo "1. Go to https://railway.app"
        echo "2. Connect your GitHub repository"
        echo "3. Add GEMINI_API_KEY environment variable"
        echo "4. Push to main branch - Railway auto-deploys!"
        echo ""
        echo "Railway will automatically use your docker-compose.yml"
        ;;

    2)
        echo ""
        echo "📋 VPS Deployment Setup:"
        echo "1. Provision VPS with Docker installed"
        echo "2. Create SSH key pair:"
        echo "   ssh-keygen -t rsa -b 4096 -C 'lexprobe-deploy'"
        echo "3. Add public key to server: ~/.ssh/authorized_keys"
        echo "4. Add these GitHub secrets:"
        echo "   - SERVER_HOST: your-server-ip"
        echo "   - SERVER_USER: root"
        echo "   - SERVER_SSH_KEY: (private key content)"
        echo "   - GEMINI_API_KEY: your-api-key"
        echo "5. Enable the deploy-vps.yml workflow"
        ;;

    3)
        echo ""
        echo "📋 Local Development:"
        echo "Run: docker-compose up --build"
        echo "Access: http://localhost:5500"
        ;;

    *)
        echo "Invalid choice. Run script again."
        exit 1
        ;;
esac

echo ""
echo "✅ Configuration complete!"
echo "📖 Check README.md for detailed instructions"