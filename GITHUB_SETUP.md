# 🚀 GitHub Setup Guide

## Step-by-Step Instructions to Get GitHub Actions Building x64 Executables

### 1. Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in (or create account)
2. Click the **"+"** in top right → **"New repository"**
3. Fill in:
   - **Repository name**: `SA32windy` (or your preferred name)
   - **Description**: "Sailaway 3 to Windy GPS Bridge"
   - **Public** or **Private** (your choice)
   - ✅ Check "Add a README file" (or use README_GITHUB.md)
   - Choose a license (optional): MIT License recommended
4. Click **"Create repository"**

### 2. Upload Your Code to GitHub

#### Option A: Using GitHub Web Interface (Easy)

1. In your new repository, click **"Add file"** → **"Upload files"**
2. Drag and drop these files:
   ```
   sailaway_to_windy.py
   QUICKSTART.md
   CONFIGURATION.md
   ARCHITECTURE.md
   STANDALONE.md
   DISTRIBUTION.md
   ARCHITECTURE_COMPATIBILITY.md
   requirements.txt
   .gitignore
   ```
3. Create a folder structure:
   - Click "Add file" → "Create new file"
   - Type: `.github/workflows/build.yml`
   - Paste contents from your local `.github/workflows/build.yml`
4. Commit the changes

#### Option B: Using Git Command Line

```bash
# Navigate to your project folder
cd "c:\Users\wildc\OneDrive\DEVELOPMENT WINDOWS FOLDER\SA32windy"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Sailaway to Windy GPS Bridge"

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/SA32windy.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Verify GitHub Actions is Enabled

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. You should see the workflow "Build Executables" running
4. Wait for it to complete (usually 2-5 minutes)

### 4. Download the x64 Executable

After the Actions workflow completes:

1. Go to **Actions** tab
2. Click on the latest workflow run
3. Scroll down to **Artifacts**
4. Download **SailawayWindyBridge-Windows-x64**
5. Extract the ZIP file
6. You now have `SailawayWindyBridge_x64.exe`! 🎉

### 5. Create a Release (Optional but Recommended)

To make it easy for users to download:

1. Go to your repository
2. Click **"Releases"** (right sidebar)
3. Click **"Create a new release"**
4. Click **"Choose a tag"** → type `v1.0.0` → **"Create new tag"**
5. **Release title**: `v1.0.0 - Initial Release`
6. **Description**:
   ```markdown
   ## Sailaway to Windy GPS Bridge v1.0.0
   
   First stable release!
   
   ### Downloads
   - **SailawayWindyBridge_x64.exe** - For most Windows PCs
   - **Source code** - Python script (works on all platforms)
   
   ### Features
   - Connect Sailaway 3 NMEA feed to Windy
   - Simple GUI for configuration
   - Real-time GPS tracking on Windy map
   
   See QUICKSTART.md for usage instructions.
   ```
7. Click **"Publish release"**

**GitHub Actions will automatically:**
- Build the x64 executable
- Attach it to your release
- Users can download directly!

### 6. Enable Manual Workflow Runs

The workflow already has `workflow_dispatch` enabled, so you can:

1. Go to **Actions** tab
2. Click **"Build Executables"** workflow
3. Click **"Run workflow"** button
4. Click the green **"Run workflow"** button
5. Build starts immediately!

### 7. Update README with Your Username

Replace `YOUR_USERNAME` in `README_GITHUB.md` with your actual GitHub username:

1. Find/replace all instances of `YOUR_USERNAME`
2. Rename `README_GITHUB.md` to `README.md` (overwrite the old one)
3. Push to GitHub

## Automatic Builds

Now, every time you:
- ✅ Push code to `main` or `master` branch
- ✅ Create a pull request
- ✅ Create a tag (like `v1.0.0`)
- ✅ Manually trigger the workflow

GitHub Actions will automatically build the **x64 executable**!

## What About ARM64?

Since GitHub doesn't have ARM64 Windows runners yet:
- Keep your local ARM64 build (`dist\SailawayWindyBridge.exe`)
- Manually upload it to releases as `SailawayWindyBridge_ARM64.exe`
- Or users can build locally on their ARM64 devices

## File Structure After Setup

```
your-repo/
├── .github/
│   └── workflows/
│       └── build.yml          # Auto-builds x64 exe
├── .gitignore
├── README.md                  # Main readme
├── QUICKSTART.md
├── CONFIGURATION.md
├── ARCHITECTURE.md
├── STANDALONE.md
├── DISTRIBUTION.md
├── ARCHITECTURE_COMPATIBILITY.md
├── requirements.txt
├── sailaway_to_windy.py       # Main script
├── build_standalone.bat       # Local build script
└── build_universal.bat        # Universal build script
```

## Troubleshooting

### Workflow Not Running?
- Check that `.github/workflows/build.yml` is in the correct path
- Verify GitHub Actions is enabled (Settings → Actions → Allow all actions)

### Build Failed?
- Click on the failed workflow
- Read the error logs
- Usually it's a path or PyInstaller issue

### Can't Push to GitHub?
- Set up Git credentials
- Or use GitHub Desktop (easier)
- Or upload files via web interface

## Benefits of This Setup

✅ **Automatic x64 builds** - No need for x64 PC  
✅ **Free** - GitHub Actions is free for public repos  
✅ **Professional** - Automated releases  
✅ **Easy updates** - Just push code, builds happen automatically  
✅ **Download artifacts** - Get x64 exe from any commit  

## Next Steps

1. Push code to GitHub
2. Wait for Actions to build
3. Download the x64 exe
4. Test it (or ask someone with x64 PC to test)
5. Create your first release
6. Share with the Sailaway community!

---

**You're all set!** 🎉

Your repository will now automatically build Windows x64 executables every time you push code!
