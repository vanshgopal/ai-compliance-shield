# AI Compliance Shield - One-Click Deploy Script
# Run this script to deploy to GitHub and Railway

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  AI Compliance Shield - Auto Deploy" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Git
Write-Host "[1/5] Checking Git..." -ForegroundColor Yellow
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Git not installed. Download from https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}
Write-Host "  OK: $gitVersion" -ForegroundColor Green

# Step 2: Initialize Git repo
Write-Host "[2/5] Initializing Git repository..." -ForegroundColor Yellow
Set-Location "C:\Users\pc\Desktop\ai-compliance-shield"
git init 2>&1 | Out-Null
git add . 2>&1 | Out-Null
git commit -m "Initial commit - AI Compliance Shield" 2>&1 | Out-Null
git branch -M main 2>&1 | Out-Null
Write-Host "  OK: Repository initialized" -ForegroundColor Green

# Step 3: Ask for GitHub username
Write-Host "[3/5] GitHub Setup..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  IMPORTANT: You need to do these steps manually:" -ForegroundColor Magenta
Write-Host "  1. Go to https://github.com/signup (create account if needed)" -ForegroundColor White
Write-Host "  2. Go to https://github.com/new" -ForegroundColor White
Write-Host "  3. Create repository named: ai-compliance-shield" -ForegroundColor White
Write-Host "  4. Make it Public" -ForegroundColor White
Write-Host ""
$username = Read-Host "  Enter your GitHub username"

if ([string]::IsNullOrEmpty($username)) {
    Write-Host "  ERROR: Username cannot be empty" -ForegroundColor Red
    exit 1
}

Write-Host "  Setting up remote..." -ForegroundColor Yellow
git remote remove origin 2>&1 | Out-Null
git remote add origin "https://github.com/$username/ai-compliance-shield.git" 2>&1 | Out-Null
Write-Host "  OK: Remote set to https://github.com/$username/ai-compliance-shield.git" -ForegroundColor Green

# Step 4: Push to GitHub
Write-Host "[4/5] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "  (A browser window will open for login - approve it)" -ForegroundColor Magenta
git push -u origin main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK: Code pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "  Push may have failed. Check if you approved the login." -ForegroundColor Yellow
}

# Step 5: Open Railway
Write-Host "[5/5] Opening Railway..." -ForegroundColor Yellow
Start-Process "https://railway.app/new"
Write-Host ""
Write-Host "  Railway is now open in your browser." -ForegroundColor Green
Write-Host "  Follow these steps:" -ForegroundColor White
Write-Host "    1. Click 'Login' -> 'Login with GitHub'" -ForegroundColor White
Write-Host "    2. Click 'New Project'" -ForegroundColor White
Write-Host "    3. Click 'Deploy from GitHub repo'" -ForegroundColor White
Write-Host "    4. Select 'ai-compliance-shield'" -ForegroundColor White
Write-Host "    5. Wait 3-5 minutes" -ForegroundColor White
Write-Host "    6. Go to Settings -> Generate Domain" -ForegroundColor White
Write-Host ""

# Final
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  DONE! Your app will be at:" -ForegroundColor Green
Write-Host "  https://$username-ai-compliance-shield.up.railway.app" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
