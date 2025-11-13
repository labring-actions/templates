# Project Context

## Purpose
This project serves as the official template repository for Sealos cloud-native application platform. It provides 159+ one-click deployment templates for popular open-source applications, enabling users to quickly deploy AI/ML tools, databases, development environments, monitoring systems, and other applications to Kubernetes clusters with minimal configuration. The templates handle complex dependencies, networking, and resource management automatically, making cloud-native application deployment accessible to developers and operations teams.

## Tech Stack
- **Kubernetes**: Container orchestration platform (StatefulSet, Service, Ingress, ConfigMap, Secret resources)
- **Docker**: Containerization technology for application packaging
- **Sealos CLI v5.1.0**: Cloud-native operating system and primary build tool
- **YAML**: Template configuration format using Kubernetes resource definitions
- **Sealos Template Engine**: Custom templating system with variable substitution and conditional rendering
- **GitHub Actions**: CI/CD pipeline for automated building and publishing
- **Shell Script**: Build automation and deployment scripts
- **GitHub Container Registry (ghcr.io)**: Container image storage
- **Alibaba Cloud OSS**: Cluster image file storage and distribution

## Project Conventions

### Code Style
- **Template File Format**: All templates follow `apiVersion: app.sealos.io/v1, kind: Template` structure
- **YAML Standards**: Follow Kubernetes resource definition standards with proper indentation and structure
- **File Naming**: Template files use kebab-case (e.g., `fastgpt.yaml`, `chatgpt-next-web.yaml`)
- **Resource Organization**: Inline templates use single file structure with `---` separators

### Template Structure Requirements
- **Metadata Section**: Required fields include title, url, gitRepo, author, description, readme, icon
- **Template Type**: Must be `inline` for integrated single-file templates
- **Categories**: Classify templates (ai, storage, database, development, monitoring, etc.)
- **Internationalization**: Support for `i18n` with multiple language variants (locale: zh/en)

### Variable System and Template Engine
- **Variable Syntax**: All variables use `${{ expression }}` format with JavaScript expression support
- **System Variables**: Built-in variables like `${{ SEALOS_NAMESPACE }}`, `${{ SEALOS_CLOUD_DOMAIN }}`, `${{ SEALOS_CERT_SECRET_NAME }}`, `${{ SEALOS_SERVICE_ACCOUNT }}`
- **System Functions**: `${{ random(n) }}` for random strings, `${{ base64(expression) }}` for encoding
- **Default Variables**: Required `app_name` with `${{ random(8) }}` suffix for uniqueness
- **Input Variables**: User-configurable parameters with type validation (string, number, boolean, choice)
- **Conditional Rendering**: `${{ if(expression) }}`, `${{ elif(expression) }}`, `${{ else() }}`, `${{ endif() }}` for dynamic content

### Required Template Fields
- **app_name defaults**: Must contain `${{ random(8) }}` for unique naming
- **metadata annotations**: Required `originImageName`, `deploy.cloud.sealos.io/minReplicas`, `deploy.cloud.sealos.io/maxReplicas`
- **resource labels**: Required `cloud.sealos.io/app-deploy-manager: ${{ defaults.app_name }}` and `app: ${{ defaults.app_name }}`
- **service naming**: NodePort services must end with `-nodeport` suffix

### Input Parameter Types and Validation
- **String**: Text input with description and default value
- **Number**: Numeric input for integer values
- **Boolean**: Toggle switch with 'true'/'false' string values
- **Choice**: Dropdown selection with options array
- **Conditional Fields**: Use `if` parameter with JavaScript expressions for dynamic form rendering

### Architecture Patterns
- **Kubernetes Resource Types**: Deployment, StatefulSet, Service, Ingress, ConfigMap, Secret, ServiceAccount, Role, RoleBinding
- **Database Integration**: KubeBlocks CRDs for managed databases (MongoDB, PostgreSQL, Redis, MySQL, Weaviate)
- **Object Storage**: Custom CRDs for bucket management with access control policies
- **Service Discovery**: Internal cluster DNS with `.${{ SEALOS_NAMESPACE }}.svc.cluster.local` pattern
- **External Access**: Ingress with automatic TLS using `${{ SEALOS_CERT_SECRET_NAME }}` or custom certificates

### Template Rendering Process
1. **Template CR Parsing**: Parse defaults (system variables only), then inputs (defaults + system variables)
2. **Application Resource Parsing**: Conditional rendering, then variable substitution with full expression support
3. **Form Generation**: Dynamic form rendering with conditional fields based on user selections
4. **Instance Creation**: Convert Template to Instance CRD with resolved variables

### Testing Strategy
- **Syntax Validation**: Sealos CLI template validation during CI/CD pipeline
- **Build Verification**: Automated cluster image creation to test template functionality
- **Variable Resolution**: Test all variable substitutions and conditional rendering
- **Resource Validation**: Verify generated Kubernetes resources are valid and deployable
- **Integration Testing**: Test database connections, service discovery, and external access

### Git Workflow
- **Branch Strategy**: Single main branch with direct PR submissions
- **Commit Conventions**:
  - Feature additions: `Add {appname} template (#pr)`
  - Bug fixes: `Fix {description} (#pr)`
  - Updates: `Update {component} in {workflow}`
- **PR Process**: All changes require review and automated testing before merge
- **Trigger Conditions**: Build triggered on template file changes to main branch or manual dispatch

## Domain Context

### Cloud-Native Application Ecosystem
- **Target Users**: Sealos platform users including developers, DevOps engineers, and system administrators
- **Application Scenarios**: Rapid deployment of open-source applications to Kubernetes environments
- **Value Proposition**: One-click deployment with automatic dependency management and standardized configurations
- **Platform Integration**: Templates optimized for Sealos cloud-native operating system features
- **Template Marketplace**: User-friendly interface for browsing and deploying applications

### Application Categories
- **AI/ML**: FastGPT, ChatGPT-Next-Web, Ollama, Dify, Lobe-Chat, and other AI tools
- **Databases**: MySQL, PostgreSQL, Redis, MongoDB, ClickHouse, and other data storage systems
- **Storage**: MinIO object storage, distributed file systems, and backup solutions
- **Development Tools**: WordPress, Drupal, Jenkins, GitLab, and development environments
- **Monitoring**: Prometheus, Grafana, Alertmanager, and observability stacks
- **Communication**: Matrix, Rocket.Chat, and collaboration tools
- **Utilities**: Various tools and utilities for system administration and productivity

### Template Development Knowledge
- **Kubernetes Expertise**: Deep understanding of resource definitions and best practices
- **Docker Containerization**: Experience with container image optimization and configuration
- **Sealos Platform**: Knowledge of Sealos-specific features, networking, and storage systems
- **Template Engine**: Proficiency with Sealos template syntax and variable system
- **Application Integration**: Experience integrating applications with databases and external services

## Important Constraints

### Technical Constraints
- **Kubernetes Compatibility**: Templates must comply with Sealos-supported K8s versions and API standards
- **Template Engine Limitations**: Template CR section doesn't support conditional rendering
- **Variable Resolution Order**: System variables → defaults → inputs → conditional rendering
- **Form Validation**: Input parameters must pass type validation and required field checks
- **Resource Naming**: Unique naming conventions to prevent conflicts in shared namespaces
- **Security Standards**: No inclusion of malicious code or known vulnerabilities

### Template Development Constraints
- **Required Fields**: `app_name` defaults with random suffix, proper metadata annotations
- **Resource Limits**: Standardized CPU (100m-1000m) and Memory (102Mi-1024Mi) constraints
- **Storage Requirements**: Use `openebs-backup` storage class for persistent volumes
- **Service Configuration**: Proper port mapping and service discovery patterns
- **External Access**: TLS termination and domain configuration for web applications

### Business Constraints
- **License Compliance**: All templates must adhere to Sealos Sustainable Use License
- **Stability Requirements**: Templates must undergo thorough testing before production release
- **Maintenance Commitment**: Regular updates to application versions and security patches
- **Documentation Quality**: Clear descriptions, usage instructions, and README links
- **User Experience**: Intuitive form inputs with helpful descriptions and validation

## External Dependencies

### Core Dependencies
- **Sealos CLI v5.1.0**: Primary build tool for cluster image creation and management
- **Sealos Template Engine**: Custom templating system with variable substitution and conditional rendering
- **GitHub Actions**: CI/CD platform for automated build and release workflows
- **GitHub Container Registry**: Primary container image storage and distribution service

### Platform Integration Dependencies
- **KubeBlocks**: Database management platform for PostgreSQL, MongoDB, Redis, MySQL
- **Sealos Object Storage**: Custom CRDs for bucket management and access control
- **Sealos Networking**: Ingress controller, DNS resolution, and service discovery
- **Certificate Management**: Automatic TLS with Let's Encrypt integration
- **Storage Classes**: OpenEBS backup storage class for persistent volumes

### Service Dependencies
- **Alibaba Cloud OSS**: Storage for cluster image tar files and distribution
- **Gitee**: Code mirror service for Chinese users and redundancy
- **Docker Hub**: Source for application container images
- **GitHub**: Source code hosting and release management
- **Let's Encrypt**: Certificate authority for automatic TLS

### Build and Automation Tools
- **jq**: JSON processing utility used in build scripts
- **curl**: File download and HTTP request utility in automation scripts
- **Shell Scripts**: Build automation and deployment orchestration
- **YAML Processors**: Template validation and format checking