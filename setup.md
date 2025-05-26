# Setting Up a GitHub Codespace with Your Repository

## Overview

GitHub Codespaces provides a cloud-based development environment that allows you to work on code directly in your browser or through VS Code desktop. This guide will walk you through forking the repository to your own account, then setting up a Python development environment within a Codespace.

## Prerequisites

- A GitHub account
- Access to GitHub Codespaces (available with GitHub Pro, Team, or Enterprise accounts, or through the free tier with usage limits)
- For local VS Code connection: VS Code installed on your machine

## Step-by-Step Setup Process

### 1. Fork the Repository

1. Navigate to the repository URL: `https://github.com/ca-carr/hackathon-EXE25.git`
2. Click the **"Fork"** button in the top-right corner of the repository page
3. Choose your personal account (or your group's organization if working as a team)
4. Optionally, rename the repository for your project
5. Click **"Create fork"**

You now have your own copy of the repository that you can modify freely.

### 2. Create a Codespace

1. From your forked repository page, click the green **"Code"** button
2. Select the **"Codespaces"** tab
3. Click **"Create codespace on main"** (or your preferred branch)

GitHub will now create and configure your cloud development environment. This process typically takes a couple of minutes.

### 3. Access Your Codespace

You have three options for accessing your Codespace:

#### Option A: Browser-Based (Default and easiest)
Once the Codespace is ready, you'll be automatically redirected to a VS Code interface running in your browser.

#### Option B: VS Code Desktop (Windows)
1. Install the **GitHub Codespaces extension** in VS Code:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "GitHub Codespaces"
   - Install the official extension by GitHub

2. Connect to your Codespace:
   - Press `Ctrl+Shift+P` to open the Command Palette
   - Type "Codespaces: Connect to Codespace"
   - Select your existing Codespace from the list
   - VS Code will download and connect to your remote environment

#### Option C: VS Code Desktop (macOS)
1. Install the **GitHub Codespaces extension** in VS Code:
   - Open VS Code
   - Go to Extensions (Cmd+Shift+X)
   - Search for "GitHub Codespaces"
   - Install the official extension by GitHub

2. Connect to your Codespace:
   - Press `Cmd+Shift+P` to open the Command Palette
   - Type "Codespaces: Connect to Codespace"
   - Select your existing Codespace from the list
   - VS Code will download and connect to your remote environment



### 4. Set Up Python Environment

#### Verify Python Installation

First, check if Python is available:

```bash
python --version
# or
python3 --version
```

#### Install Project Dependencies

Most Python projects include a `requirements.txt` file or use other dependency management tools. Look for one of these files in the repository:

**If `requirements.txt` exists:**
```bash
pip install -r requirements.txt
```



### 5. Verify Installation

Test that your environment is properly configured:

```bash
python -c "import sys; print(sys.version)"
```

Run any test scripts or initial commands specified in the repository's README file.

## Security Considerations for Local Connections

- **Secure tunnel encryption**: All communication between your local VS Code and the Codespace is encrypted
- **Authentication**: Uses your GitHub credentials for secure access
- **Network isolation**: The remote environment remains isolated from your local machine's file system
- **Audit logging**: GitHub maintains logs of Codespace access and usage

## Best Practices and Security Considerations

### Environment Security

- **Never commit sensitive data** like API keys, passwords, or credentials to the repository
- Use environment variables for configuration secrets
- Review the repository's `.gitignore` file to ensure sensitive files are excluded

### Development Workflow

- **Create a new branch** for your work rather than working directly on main:
  ```bash
  git checkout -b feature/your-feature-name
  ```

- **Regularly commit and push** your changes:
  ```bash
  git add .
  git commit -m "Descriptive commit message"
  git push origin feature/your-feature-name
  ```

### Resource Management

- **Stop your Codespace** when not in use to conserve usage limits
- **Delete unused Codespaces** to free up storage quota
- Monitor your usage through GitHub settings
- **Disconnect from VS Code** when finished to ensure proper resource cleanup

## Troubleshooting

### Common Issues

**VS Code Connection Problems:**
- Ensure the GitHub Codespaces extension is installed and up to date
- Try refreshing the connection: `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (macOS) → "Developer: Reload Window"
- Check your internet connection stability

**Python version conflicts:**
- Use `python3` instead of `python` if you encounter version issues
- Check if the project specifies a particular Python version in `.python-version` or similar files

**Permission errors:**
- Ensure you have proper access to the repository
- Check if the repository requires specific GitHub permissions

**Package installation failures:**
- Update pip: `pip install --upgrade pip`
- Clear pip cache: `pip cache purge`
- Try installing packages individually to isolate problematic dependencies

## Additional Resources

- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)
- [Python Virtual Environments Best Practices](https://docs.python.org/3/tutorial/venv.html)


