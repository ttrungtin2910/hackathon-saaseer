#!/bin/bash
# Deploy script for SaaSeer Contract Management API

echo "🚀 SaaSeer Contract Management API - Deployment Script"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized"
    echo "💡 Run: git init"
    exit 1
fi

# Check git status
echo "📋 Checking git status..."
git status --short

# Add all files
echo "📁 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "feat: Update SaaSeer Contract Management API

- Enhanced null values support
- Improved error handling
- Updated documentation
- Clean project structure"

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ Remote repository exists"
    echo "📤 Pushing to remote..."
    git push origin main
else
    echo "📝 No remote repository found"
    echo "💡 To add a remote repository:"
    echo "   git remote add origin <repository-url>"
    echo "   git push -u origin main"
fi

echo "✅ Deployment script completed!"
echo "🌐 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
