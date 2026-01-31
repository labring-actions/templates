# Contributing to Sealos Template Repository

Thank you for your interest in contributing to the Sealos Template Repository! This document provides guidelines and instructions for contributing templates, documentation, or improvements.

## 🎯 Types of Contributions

We welcome contributions in these areas:

- **New application templates** - Add support for new applications
- **Template improvements** - Optimize existing templates (better defaults, resources, etc.)
- **Documentation** - Improve guides, fix typos, add examples
- **Bug fixes** - Fix issues in templates or documentation
- **Translations** - Improve or add translations for documentation

## 📝 Adding a New Template

### Prerequisites

1. The application must be actively maintained
2. The Docker image must be publicly available (Docker Hub, GHCR, etc.)
3. The application should be production-ready
4. You have tested the template on Sealos

### Step-by-Step Guide

#### 1. Prepare Your Template

```bash
# Fork and clone this repository
git clone https://github.com/your-username/templates.git
cd templates

# Create a new branch
git checkout -b add-my-awesome-app

# Copy the reference template
cp template.yaml template/my-awesome-app.yaml
```

#### 2. Customize the Template

Edit `template/my-awesome-app.yaml`:

```yaml
spec:
  title: "My Awesome App"               # Display name
  url: "https://myapp.example.com"     # Official website
  gitRepo: "https://github.com/myuser/my-awesome-app"  # Source code
  author: "your-name"                   # Your name
  description: "Brief description of what this app does"
  readme: "https://raw.githubusercontent.com/.../README.md"  # Optional
  icon: "https://..."                   # App icon URL (recommended size: 96x96)
```

#### 3. Configure the Application

- **Docker image**: Use a specific version tag (e.g., `v1.2.3`), avoid `latest`
- **Environment variables**: Set required env vars, document optional ones
- **Resource limits**: Adjust CPU/memory based on actual needs
- **Persistent storage**: Configure if the app needs data persistence
- **Ports**: Expose only necessary ports (typically 80 for web apps)

#### 4. Test Your Template

1. Upload your template to your fork
2. Deploy it on Sealos to verify it works
3. Test all user inputs and configurations
4. Verify data persistence (if applicable)
5. Check that the app is accessible via Ingress

#### 5. Submit Your PR

```bash
git add template/my-awesome-app.yaml
git commit -m "Add template for My Awesome App"
git push origin add-my-awesome-app
```

Then open a Pull Request with:
- Clear title: `Add template for My Awesome App`
- Description: Include app info, test results, and any notes

### Template Guidelines

#### Naming Convention
- **Filename**: Lowercase, hyphen-separated (e.g., `my-awesome-app.yaml`)
- **App name in defaults**: Descriptive prefix with random suffix (e.g., `myawesomeapp-${{ random(8) }}`)

#### Required Fields
```yaml
spec:
  title: ""           # App display name
  url: ""             # Official website
  gitRepo: ""         # Source repository
  author: ""          # Maintainer
  description: ""     # Brief description (1-2 sentences)
  icon: ""            # App icon URL
```

#### Best Practices

- **Specific image versions**: Use tags like `v1.2.3`, not `latest`
- **Reasonable defaults**: Set sensible values for all inputs
- **Clear descriptions**: Explain what each input does
- **Resource efficiency**: Don't over-allocate CPU/memory
- **Security**: Don't expose unnecessary ports or services
- **Documentation**: Link to official docs in `readme` field

#### Example Template Structure

```yaml
---
apiVersion: app.sealos.io/v1
kind: Template
metadata:
  name: ${{ defaults.app_name }}
spec:
  title: "Example App"
  url: "https://example.com"
  gitRepo: "https://github.com/user/example-app"
  author: "Your Name"
  description: "An example application template"
  readme: "https://raw.githubusercontent.com/.../README.md"
  icon: "https://example.com/icon.png"
  templateType: inline
  
  defaults:
    app_name:
      type: string
      value: exampleapp-${{ random(8) }}
    app_host:
      type: string
      value: ${{ random(8) }}
  
  inputs:
    admin_password:
      description: "Admin account password"
      type: string
      required: true
    api_key:
      description: "API key for external service"
      type: string
      required: false
      default: ""

---
# Kubernetes resources (StatefulSet, Service, Ingress)
apiVersion: apps/v1
kind: StatefulSet
# ... rest of the configuration
```

## 🐛 Bug Fixes & Improvements

### Reporting Issues

When reporting a bug, please include:
- Template name
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots/logs if applicable

### Submitting Fixes

1. Create an issue to discuss the fix (if it's not trivial)
2. Create a branch for your fix: `git checkout -b fix-template-name-issue`
3. Make your changes and test thoroughly
4. Submit a PR with clear description

## 📖 Documentation Contributions

### Improving Documentation

- Fix typos and grammar
- Clarify confusing sections
- Add examples or use cases
- Improve structure and formatting
- Add diagrams or visual aids

### Adding Examples

If you have a complex use case that would benefit from an example:
1. Create a new file in the `docs/` directory
2. Document the scenario clearly
3. Provide step-by-step instructions
4. Link it from the main README

## 🤝 Code of Conduct

- Be respectful and constructive
- Focus on what is best for the community
- Show empathy towards other community members
- Accept feedback gracefully

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Template has been tested on Sealos
- [ ] All required fields are filled
- [ ] Docker image uses a specific version tag (not `latest`)
- [ ] Resource limits are reasonable
- [ ] Documentation is clear and accurate
- [ ] PR description explains the changes
- [ ] No unrelated changes are included

## 🎉 Recognition

Contributors will be recognized in:
- The repository's contributors list
- Release notes (for significant contributions)
- Optional: Author attribution in template metadata

## 📧 Getting Help

- **Discussions**: [GitHub Discussions](https://github.com/labring-actions/templates/discussions)
- **Issues**: [GitHub Issues](https://github.com/labring-actions/templates/issues)
- **Discord**: [Sealos Discord Server](https://discord.gg/sealos)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the repository.

---

Thank you for contributing! 🙏
