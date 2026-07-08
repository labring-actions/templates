# Sealos Template Repository

[简体中文](README_zh.md) | [Quick Deploy](https://os.sealos.io)

This repository is the source for Sealos App Store templates. Use the published templates to deploy applications quickly, or add a new `template/<app-name>/` directory to contribute an application template.

![](docs/images/homepage.png)

## 🚀 Quick Start

### Deploy Your First App

1. **Browse available templates** in the [Sealos App Store](https://sealos.io/products/app-store) or the [`template/`](template/) directory.
2. **Open the template documentation** and click the "Deploy on Sealos" button.
3. **Configure and deploy** by filling in the required parameters.

Template authoring quick links:
- Start from [template.yaml](template.yaml) and place the finished file at `template/<app-name>/index.yaml`.
- Add `README.md`, `README_zh.md`, an icon, and `website-screenshot.webp` next to the template file.
- Built-in variables/functions use `GitHub Actions`-style syntax; see [example.md](example.md).
- A complete FastGPT example and database Cluster YAML examples (MongoDB/PostgreSQL/MySQL/Redis/Kafka/Milvus/ClickHouse) are in [example.md](example.md).

Your app will be running in minutes.

### Popular Templates

| Template | Description | Deploy |
|----------|-------------|--------|
| FastGPT | Build your own knowledge base with AI | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/fastgpt) |
| ChatGPT-Next-Web | ChatGPT web UI with your own API key | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/chatgpt-next-web) |
| Code-Server | VS Code in your browser | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/code-server) |
| Cloudreve | Cloud storage system | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/cloudreve) |
| Appsmith | Low-code app builder | [![Deploy](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/appsmith) |

[View all templates →](template/)

## 📚 Documentation

- **[How to create a template](#how-to-create-a-template)** - Create your own application template
- **[Template usage tutorial](https://os.sealos.io)** - Step-by-step guide for using templates
- **[example.md](example.md)** - Detailed template development guide
- **[template.yaml](template.yaml)** - Template reference file

## 🛠️ How to Create a Template

Create a template by adding a directory under `template/<app-name>/`. Each template directory should contain the deployable YAML, user-facing documentation, and visual assets used by the App Store.

### 1. Start from a template reference

Copy [template.yaml](template.yaml) into a new app directory:

```bash
mkdir -p template/my-app
cp template.yaml template/my-app/index.yaml
```

Update the metadata, image references, inputs, resource names, readme links, icon, and screenshot URLs for your application.

### 2. Add the required files

A complete template directory usually includes:

```text
template/my-app/
├── index.yaml
├── README.md
├── README_zh.md
├── logo.png
└── website-screenshot.webp
```

Use `logo.svg` or another image format when it fits the upstream project asset better. Keep the English and Chinese READMEs focused on how the deployed app is used on Sealos.

### 3. Understand the structure

Template files are divided into two main parts:

- **Metadata CR**: Template information, default values, and user inputs
- **Kubernetes Resources**: StatefulSet, Service, Ingress, etc.

For detailed explanation, see [example.md](example.md).

### 4. Use variables and functions

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

### 5. Review a complete example

The [FastGPT](example.md) example demonstrates how to create a complete template with:
- Default application name and hostname
- User-configurable inputs (API key, password, database type)
- Multiple Kubernetes resources (database, application, ingress)

## 🔗 Use "Deploy on Sealos" Button

You can add a "Deploy on Sealos" button to your project's README:

### Markdown

```markdown
[![](https://sealos.io/Deploy-on-Sealos.svg)](https://sealos.io/products/app-store/your-app-name)
```

### HTML

```html
<a href="https://sealos.io/products/app-store/your-app-name">
  <img src="https://sealos.io/Deploy-on-Sealos.svg" alt="Deploy on Sealos"/>
</a>
```

Replace `your-app-name` with your template's `metadata.name` from the Template CR.

## 🤝 Contributing

We welcome contributions! Follow these steps:

1. **Fork** this repository
2. **Create a branch** for your template or improvement
3. **Add or update one `template/<app-name>/` directory**
4. **Test your template** on Sealos before submitting
5. **Submit a pull request** with a clear description and verification notes

### Template Guidelines

- **Naming**: Use lowercase, hyphen-separated names (e.g., `my-awesome-app`)
- **Description**: Write clear, concise descriptions
- **Documentation**: Include English and Chinese usage instructions
- **Assets**: Include an icon and a current application screenshot
- **Defaults**: Provide sensible default values for all inputs
- **Resources**: Set reasonable resource limits (CPU/memory)

## 📖 Resources

- [Sealos Documentation](https://sealos.io/docs)
- [Sealos App Store](https://sealos.io/products/app-store)
- [Issues](https://github.com/labring-actions/templates/issues) - Report bugs or request features
- [Discussions](https://github.com/labring-actions/templates/discussions) - Ask questions and share ideas

## 📄 License

This repository follows the Sealos project license.
