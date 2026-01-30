# Sealos Template Repository

[简体中文](README_zh.md) | [在线使用](https://cloud.sealos.io/?openapp=system-fastdeploy%3F)

With the templates in this repository, you can easily run various applications on Sealos without worrying about dependencies between applications. Deploy with one click!

![](docs/images/homepage.png)

## 🚀 Quick Start

### 3 Steps to Deploy Your First App

1. **Browse available templates** and find one you like
2. **Click the "Deploy on Sealos" button** in the template documentation
3. **Configure and deploy** - just fill in the required parameters

That's it! Your app will be running in minutes.

### Popular Templates

| Template | Description | Deploy |
|----------|-------------|--------|
| FastGPT | Build your own knowledge base with AI | [![Deploy](Deploy-on-Sealos.svg)](https://cloud.sealos.io/?openapp=system-fastdeploy%3FtemplateName%3Dfastgpt) |
| ChatGPT-Next-Web | ChatGPT web UI with your own API key | [![Deploy](Deploy-on-Sealos.svg)](https://cloud.sealos.io/?openapp=system-fastdeploy%3FtemplateName%3Dchatgpt-next-web) |
| Code-Server | VS Code in your browser | [![Deploy](Deploy-on-Sealos.svg)](https://cloud.sealos.io/?openapp=system-fastdeploy%3FtemplateName%3Dcode-server) |
| Cloudreve | Cloud storage system | [![Deploy](Deploy-on-Sealos.svg)](https://cloud.sealos.io/?openapp=system-fastdeploy%3FtemplateName%3Dcloudreve) |
| Appsmith | Low-code app builder | [![Deploy](Deploy-on-Sealos.svg)](https://cloud.sealos.io/?openapp=system-fastdeploy%3FtemplateName%3Dappsmith) |

[View all templates →](template/)

## 📚 Documentation

- **[How to create a template](#how-to-create-a-template)** - Create your own application template
- **[Template usage tutorial](https://cloud.sealos.io/?openapp=system-fastdeploy%3F)** - Step-by-step guide for using templates
- **[example.md](example.md)** - Detailed template development guide
- **[template.yaml](template.yaml)** - Template reference file

## 🛠️ How to Create a Template

You can create your application template through existing template files or the UI (TODO button).

### 1. Start from a template reference

Copy [template.yaml](template.yaml) as your starting point:

```bash
cp template.yaml my-app-template.yaml
```

### 2. Understand the structure

Template files are divided into two main parts:

- **Metadata CR**: Template information, default values, and user inputs
- **Kubernetes Resources**: StatefulSet, Service, Ingress, etc.

For detailed explanation, see [example.md](example.md).

### 3. Use variables and functions

The system provides built-in environment variables and functions. Use `GitHub Actions`-like syntax:

```yaml
# System built-in variable
${{ SEALOS_NAMESPACE }}

# Function to generate random string
${{ random(8) }}

# User input variable
${{ inputs.your_parameter }}
```

See [Built-in system variables and functions](example.md#built-in-system-variables-and-functions) for complete reference.

### 4. Example: FastGPT Template

The [FastGPT](example.md) example demonstrates how to create a complete template with:
- Default application name and hostname
- User-configurable inputs (API key, password, database type)
- Multiple Kubernetes resources (database, application, ingress)

## 🔗 Use "Deploy on Sealos" Button

You can add a "Deploy on Sealos" button to your project's README:

### Markdown

```markdown
[![](https://raw.githubusercontent.com/labring-actions/templates/main/Deploy-on-Sealos.svg)](https://cloud.sealos.io/?openapp=system-fastdeploy%3FtemplateName%3Dyour-app-name)
```

### HTML

```html
<a href="https://cloud.sealos.io/?openapp=system-fastdeploy%3FtemplateName%3Dyour-app-name">
  <img src="https://raw.githubusercontent.com/labring-actions/templates/main/Deploy-on-Sealos.svg" alt="Deploy on Sealos"/>
</a>
```

Replace `your-app-name` with your template's `metadata.name` from the Template CR.

## 🤝 Contributing

We welcome contributions! Follow these steps:

1. **Fork** this repository
2. **Create a branch** for your template or improvement
3. **Follow the template structure** - use [template.yaml](template.yaml) as reference
4. **Test your template** on Sealos before submitting
5. **Submit a pull request** with clear description

### Template Guidelines

- **Naming**: Use lowercase, hyphen-separated names (e.g., `my-awesome-app`)
- **Description**: Write clear, concise descriptions
- **Documentation**: Include app-specific usage instructions if needed
- **Defaults**: Provide sensible default values for all inputs
- **Resources**: Set reasonable resource limits (CPU/memory)

## 📖 Resources

- [Sealos Documentation](https://sealos.io/docs)
- [Sealos Template Market](https://cloud.sealos.io/?openapp=system-fastdeploy%3F)
- [Issues](https://github.com/labring-actions/templates/issues) - Report bugs or request features
- [Discussions](https://github.com/labring-actions/templates/discussions) - Ask questions and share ideas

## 📄 License

This repository follows the same license as Sealos. See [LICENSE](LICENSE) for details.
