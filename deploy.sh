#!/bin/bash

# LexProbe Deployment Script

echo "🚀 Deploying LexProbe..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check for required environment variables
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY environment variable not set"
    exit 1
fi

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ LexProbe deployed successfully!"
    echo ""
    echo "🌐 Services:"
    echo "  - Frontend: http://localhost:5500"
    echo "  - Backend API: http://localhost:8000"
    echo "  - Qdrant: http://localhost:6333"
    echo ""
    echo "📊 View logs: docker-compose logs -f"
    echo "🛑 Stop: docker-compose down"
else
    echo "❌ Deployment failed. Check logs:"
    docker-compose logs
    exit 1
fi