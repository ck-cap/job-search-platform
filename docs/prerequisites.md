# Prerequisites Installation Guide

This guide will help you install all the required software to run the Job Search Platform. Follow these steps even if you're completely new to development.

## What You Need to Install

1. **Docker Desktop** - For running the backend services
2. **Node.js & pnpm** - For the frontend development
3. **Git** (optional) - For cloning the repository
4. **Google API Key** - For AI functionality

---

## 1. Install Docker Desktop

Docker runs our backend services in containers.

### Windows
1. Go to [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Click **"Download for Windows"**
3. Run the downloaded `Docker Desktop Installer.exe`
4. Follow the installation wizard (keep default settings)
5. **Restart your computer** when prompted
6. After restart, Docker Desktop should start automatically
7. **Verify installation**:
   - Open Command Prompt (Windows key + R, type `cmd`, press Enter)
   - Type: `docker --version`
   - You should see something like: `Docker version 24.0.6`

### Mac
1. Go to [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Click **"Download for Mac"** 
   - Choose **Intel chip** or **Apple chip** based on your Mac
   - Not sure? Click Apple menu → About This Mac to check
3. Open the downloaded `.dmg` file
4. Drag Docker to your Applications folder
5. Open Docker from Applications
6. Click **"Open"** when prompted about security
7. Follow the setup wizard
8. **Verify installation**:
   - Open Terminal (Spotlight search: "Terminal")
   - Type: `docker --version`
   - You should see something like: `Docker version 24.0.6`

### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again
sudo apt update

# Install Docker
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add your user to docker group (so you don't need sudo)
sudo usermod -aG docker $USER

# Log out and log back in, then verify
docker --version
```

---

## 2. Install Node.js & pnpm

Node.js runs JavaScript on your computer. pnpm is a fast package manager.

### Method 1: Using Node.js Official Installer (Easiest)

#### Windows & Mac
1. Go to [nodejs.org](https://nodejs.org/)
2. Download the **LTS version** (Long Term Support - more stable)
3. Run the installer
4. Keep all default settings during installation
5. **Verify Node.js installation**:
   - Windows: Open Command Prompt
   - Mac: Open Terminal
   - Type: `node --version`
   - You should see something like: `v20.10.0`

#### Install pnpm after Node.js
```bash
# Install pnpm globally
npm install -g pnpm

# Verify pnpm installation
pnpm --version
```

#### Additional Setup for Windows Users
**Important for Windows users:** You may need to install `cross-env` to run frontend development scripts seamlessly. This package ensures environment variables work correctly across different operating systems.

```bash
# Install cross-env globally using pnpm
pnpm add -g cross-env

# Verify installation
cross-env --version
```

**Note:** If you encounter issues with environment variable scripts on Windows (like `NUXT_PUBLIC_API_BASE_URL=... nuxt dev`), make sure `cross-env` is installed and properly configured.

**Script Modification for Windows:**
After installing `cross-env`, you may need to update the pnpm scripts in `services/frontend/package.json` to use `cross-env`. Look for scripts that set environment variables and modify them as follows:

```json
// Before (won't work on Windows):
"dev": "NUXT_PUBLIC_API_BASE_URL=http://localhost:8000 nuxt dev",
"dev:local": "NUXT_PUBLIC_API_BASE_URL=http://localhost:8000 nuxt dev"

// After (works on all platforms):
"dev": "cross-env NUXT_PUBLIC_API_BASE_URL=http://localhost:8000 nuxt dev",
"dev:local": "cross-env NUXT_PUBLIC_API_BASE_URL=http://localhost:8000 nuxt dev"
```

**Steps to update scripts:**
1. Navigate to `services/frontend/package.json`
2. Find scripts that start with environment variables (like `NUXT_PUBLIC_API_BASE_URL=...`)
3. Add `cross-env ` at the beginning of those script commands
4. Save the file

This ensures the frontend development commands work seamlessly on Windows, Mac, and Linux.

### Method 2: Using Node Version Manager (Advanced)

This method lets you install multiple Node.js versions.

#### Mac/Linux - Install nvm
```bash
# Download and install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal or run:
source ~/.bashrc

# Install latest LTS Node.js
nvm install --lts

# Use the installed version
nvm use --lts

# Install pnpm
npm install -g pnpm
```

#### Windows - Install nvm-windows
1. Go to [nvm-windows releases](https://github.com/coreybutler/nvm-windows/releases)
2. Download `nvm-setup.exe` from the latest release
3. Run the installer
4. Open a new Command Prompt as Administrator
5. Install Node.js:
   ```cmd
   nvm install lts
   nvm use lts
   npm install -g pnpm
   ```

---

## 3. Install Git (Optional but Recommended)

Git helps you download and manage code.

### Windows
1. Go to [git-scm.com](https://git-scm.com/)
2. Click **"Download for Windows"**
3. Run the installer
4. **Important settings during installation**:
   - Default editor: Choose "Use Visual Studio Code" or "Use Notepad++"
   - Line ending conversions: Choose "Checkout Windows-style, commit Unix-style"
   - Keep other settings as default
5. **Verify installation**:
   - Open Command Prompt
   - Type: `git --version`

### Mac
Git is usually pre-installed. To check:
```bash
git --version
```

If not installed:
```bash
# Install using Homebrew (if you have it)
brew install git

# Or download from git-scm.com
```

### Linux
```bash
# Ubuntu/Debian
sudo apt install git

# CentOS/RHEL/Fedora
sudo yum install git
# or
sudo dnf install git
```

---

## 4. Get Google API Key

The platform uses Google's AI for resume analysis.

### Step-by-Step Instructions

1. **Go to Google AI Studio**:
   - Open your web browser
   - Go to: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

2. **Sign in to Google**:
   - Use your Google account (Gmail, etc.)
   - If you don't have one, create a Google account first

3. **Create API Key**:
   - Click **"Create API Key"**
   - Choose **"Create API key in new project"** (recommended)
   - Wait a few seconds for the key to be generated

4. **Copy Your API Key**:
   - You'll see a long string like: `AIzaSyD...` (about 40 characters)
   - Click the **copy button** or select all and copy
   - **Keep this safe** - don't share it publicly!

5. **Important Notes**:
   - This API key gives access to Google's AI services
   - Keep it private (don't put it in public code)
   - We'll use this later in the setup

---

## 5. Environment Variables Configuration

After completing the setup, you'll need to configure environment variables in your `.env` file. Most variables have default values, but here are some important notes:

### MODEL_PATH and DATASET_PATH
These variables specify the paths to the machine learning model and dataset files used for job matching:

```bash
MODEL_PATH=/app/model/fine_tuned_mpnet_with_eval
DATASET_PATH=/app/dataset/mpnet_finetune_dataset_test.csv
```

**Important Notes:**
- ⚠️ **Only modify these paths if you need to use different model or dataset files**
- The default paths work with the provided Docker setup and should not be changed for standard usage
- These paths are mapped to Docker volumes, so changing them requires corresponding changes in the Docker configuration
- If you're using custom models or datasets, ensure the files exist at the specified paths before starting the services

### Additional Environment Variable Considerations
- **GOOGLE_API_KEY**: This is required and must be set with your actual Google AI API key
- **NUXT_PUBLIC_API_BASE_URL**: Automatically set by development scripts, typically points to `http://localhost:8000`
- Most other environment variables have sensible defaults and don't require modification for standard development

---

## 6. Verify Everything is Installed

Open your terminal/command prompt and run these commands:

```bash
# Check Docker
docker --version
# Should show: Docker version 24.x.x

# Check Node.js
node --version
# Should show: v20.x.x or similar

# Check pnpm
pnpm --version
# Should show: 8.x.x or similar

# Check Git (optional)
git --version
# Should show: git version 2.x.x
```

If all commands work, you're ready! 🎉

---

## Troubleshooting

### Docker Issues
- **"Docker command not found"**: Restart your computer after installation
- **Permission denied**: 
  - Windows: Run Command Prompt as Administrator
  - Linux: Add user to docker group (see Linux install steps)
- **Docker Desktop won't start**: Check if virtualization is enabled in BIOS

### Node.js/pnpm Issues
- **"Command not found"**: Restart terminal after installation
- **Permission errors**: Use `sudo` on Mac/Linux for global installs
- **Old version**: Uninstall old Node.js first, then reinstall

### General Tips
- **Restart your terminal** after installing anything
- **Restart your computer** if commands still don't work
- **Check system requirements** - make sure your OS version is supported
- **Disable antivirus temporarily** if installations fail

---

## Next Steps

Once everything is installed:

1. **Download the project** (if you haven't already)
2. **Follow the [Setup Guide](setup.md)** to configure and run the platform
3. **Check the [Development Guide](development.md)** if you want to modify the code

---

*Need help? Check our [Development Guide](development.md) for more troubleshooting tips.* 