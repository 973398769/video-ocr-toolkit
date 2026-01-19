# GitHub Setup Instructions

## 1. Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Repository name: `video-ocr-toolkit`
4. Description: `A powerful toolkit for extracting and annotating text from videos using OCR`
5. Choose "Public"
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## 2. Push to GitHub

```bash
cd ~/Documents/video-ocr-toolkit

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/video-ocr-toolkit.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 3. Update README.md Links

After creating the repository, update these links in README.md:

- Replace `your-username` with your actual GitHub username in:
  - Clone URL
  - Issue link
  - Any other GitHub URLs

## 4. Add Topics (Optional but Recommended)

On your GitHub repository page:
1. Click "Add topics"
2. Add these topics:
   - `ocr`
   - `video-processing`
   - `text-extraction`
   - `computer-vision`
   - `easyocr`
   - `opencv`
   - `python`
   - `video-annotation`

## 5. Enable GitHub Pages (Optional)

If you want to create a project website:
1. Go to repository Settings
2. Scroll to "GitHub Pages"
3. Select source: `main` branch
4. Choose folder: `/ (root)`

## 6. Add Shields/Badges (Optional)

The README already includes:
- License badge
- Python version badge

You can add more at [shields.io](https://shields.io):
- GitHub stars
- GitHub forks
- GitHub issues
- Build status (if you add CI/CD)

## 7. Repository Settings

Recommended settings:
- ✅ Issues enabled
- ✅ Wiki disabled (use README instead)
- ✅ Discussions disabled (use Issues)
- ✅ Projects disabled
- ✅ Security: Enable Dependabot alerts

## Example Commands

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/video-ocr-toolkit.git

# Update repository
git add .
git commit -m "Update documentation"
git push origin main

# Create a new branch for features
git checkout -b feature/new-tool
git push origin feature/new-tool
```

## Share Your Project

After publishing, share on:
- Reddit: r/Python, r/computervision, r/opencv
- Twitter/X with hashtags: #Python #OCR #ComputerVision
- LinkedIn
- Hacker News
- Dev.to

## Star and Watch

Don't forget to:
1. Star your own repository (others will see it's active)
2. Watch the repository to get notifications
