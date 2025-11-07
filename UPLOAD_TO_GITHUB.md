# 🚀 Easy Upload to GitHub (No Git Required!)

## Your Repository
https://github.com/mikeywildcat/SA32windy

## Step-by-Step Upload Instructions

### Step 1: Prepare Your Files

You need to upload these files to GitHub:

**Main Files:**
- ✅ `sailaway_to_windy.py`
- ✅ `LICENSE`
- ✅ `.gitignore`
- ✅ `requirements.txt`

**Documentation:**
- ✅ `QUICKSTART.md`
- ✅ `CONFIGURATION.md`
- ✅ `ARCHITECTURE.md`
- ✅ `STANDALONE.md`
- ✅ `DISTRIBUTION.md`
- ✅ `ARCHITECTURE_COMPATIBILITY.md`

**Scripts:**
- ✅ `build_standalone.bat`
- ✅ `build_universal.bat`
- ✅ `run_bridge.bat`
- ✅ `setup_git.bat`

### Step 2: Upload Files via Web

1. **Go to your repository**: https://github.com/mikeywildcat/SA32windy

2. **Click "Add file" → "Upload files"**

3. **Drag and drop ALL the files listed above** into the upload area

4. **Scroll down and click "Commit changes"**

### Step 3: Create the GitHub Actions Workflow

This is the important part for automatic x64 builds!

1. **In your repository, click "Add file" → "Create new file"**

2. **In the filename box, type exactly:**
   ```
   .github/workflows/build.yml
   ```
   (This will automatically create the folders)

3. **Copy and paste this entire content:**

```yaml
name: Build Executables

on:
  push:
    branches: [ main, master ]
    tags:
      - 'v*'
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # Allows manual trigger

jobs:
  build-windows-x64:
    name: Build Windows x64 (Intel/AMD)
    runs-on: windows-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python 3.12
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller
        
    - name: Build x64 executable
      run: |
        pyinstaller --onefile --windowed --name "SailawayWindyBridge_x64" sailaway_to_windy.py
        
    - name: Verify build
      run: |
        if (Test-Path "dist\SailawayWindyBridge_x64.exe") {
          Write-Host "✓ Build successful!"
          $size = (Get-Item "dist\SailawayWindyBridge_x64.exe").Length / 1MB
          Write-Host "File size: $([math]::Round($size, 2)) MB"
        } else {
          Write-Host "✗ Build failed!"
          exit 1
        }
        
    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: SailawayWindyBridge-Windows-x64
        path: dist/SailawayWindyBridge_x64.exe
        retention-days: 90
        
    - name: Create Release (if tagged)
      if: startsWith(github.ref, 'refs/tags/v')
      uses: softprops/action-gh-release@v1
      with:
        files: |
          dist/SailawayWindyBridge_x64.exe
          README.md
          QUICKSTART.md
          STANDALONE.md
        body: |
          ## Sailaway to Windy GPS Bridge ${{ github.ref_name }}
          
          ### Downloads
          - **SailawayWindyBridge_x64.exe** - For most Windows PCs (Intel/AMD)
          - For ARM64 Windows, download the Python script and run locally
          
          ### What's New
          See CHANGELOG for details.
          
          ### Installation
          1. Download the .exe for your system
          2. Double-click to run
          3. See QUICKSTART.md for usage instructions
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

4. **Scroll down and click "Commit changes"**

### Step 4: Update README

1. **Open `README_GITHUB.md` from your local files**

2. **Find/Replace all instances of `YOUR_USERNAME` with `mikeywildcat`**

3. **Save the file**

4. **In your GitHub repo, click "Add file" → "Upload files"**

5. **Upload the modified `README_GITHUB.md`**

6. **After upload, rename it to `README.md`**:
   - Click on the file
   - Click the pencil icon (Edit)
   - Change filename from `README_GITHUB.md` to `README.md`
   - Commit changes

### Step 5: Watch the Magic! ✨

1. **Go to the "Actions" tab** in your repository

2. **You should see "Build Executables" workflow running**

3. **Wait 3-5 minutes for it to complete**

4. **Download your x64 executable**:
   - Click on the completed workflow
   - Scroll to "Artifacts"
   - Download `SailawayWindyBridge-Windows-x64.zip`
   - Extract it to get `SailawayWindyBridge_x64.exe`

### Step 6: Add Your ARM64 Build (Optional)

1. **Create a release**:
   - Go to "Releases" tab
   - Click "Create a new release"
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - Initial Release`

2. **Upload your local ARM64 build**:
   - Drag your `dist\SailawayWindyBridge.exe` to the release
   - Rename it to `SailawayWindyBridge_ARM64.exe`

3. **The x64 build will be automatically attached by GitHub Actions!**

4. **Publish the release**

## What Gets Built Automatically

Every time you upload files or make changes:
- ✅ GitHub Actions builds `SailawayWindyBridge_x64.exe`
- ✅ Available in Actions → Artifacts
- ✅ Automatically attached to releases when you tag

## No Git Installation Needed!

You can manage everything through the GitHub web interface:
- ✅ Upload files
- ✅ Edit files
- ✅ Create releases
- ✅ Download built executables

## Quick Reference

**Your repo**: https://github.com/mikeywildcat/SA32windy
**Upload files**: Click "Add file" → "Upload files"
**View Actions**: Click "Actions" tab
**Create release**: Click "Releases" → "Create a new release"

---

**You're all set!** Just follow the steps above and your x64 executable will build automatically! 🎉
