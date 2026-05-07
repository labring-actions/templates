---
name: sealos-readme-writer
description: Create professional README documentation for Sealos application templates. Use this skill when creating or updating README.md files for Sealos templates in the template/ directory, or when a bilingual README is required. Generates comprehensive documentation following Sealos template standards including deployment guides, architecture details, use cases, platform-specific features, and a Chinese README_zh.md produced via english-to-chinese-translator after the English README is complete.
---

# Sealos README Writer

## Overview

This skill provides a standardized template and guidelines for creating high-quality README documentation for Sealos application templates. It ensures consistent, professional documentation that helps users understand, deploy, and manage applications on the Sealos platform.

## When to Use This Skill

Use this skill when:
- Creating a new README.md file for a Sealos application template
- Updating existing README documentation to meet current standards
- A user asks to document a Sealos template
- Working in a `template/<app-name>/` directory and documentation is needed

## README Structure

All Sealos template READMEs should follow this structure:

### 1. Title and Introduction

Start with a clear H1 title following this format:

```markdown
# Deploy and Host [Application Name] on Sealos
```

Follow with a one-sentence description of what the application does and how it's deployed:

```markdown
[Application Name] is [brief one-sentence description]. This template deploys [Application Name] [with architecture details] on Sealos Cloud.
```

If available, include a screenshot:

```markdown
![Application Screenshot](screenshot-url)
```

### 2. About Hosting [Application Name]

Provide 2-3 paragraphs explaining:
- How the application works
- Architecture components (for multi-service deployments)
- Key features and capabilities
- What Sealos automatically provisions (databases, storage, etc.)

**Example:**
```markdown
## About Hosting Typesense

Typesense runs as a single-node search engine service that provides instant search results with typo tolerance and faceting capabilities. The Sealos template automatically provisions persistent storage for your search indices and data, ensuring your search data is safely stored and survives restarts.

The deployment includes automatic SSL certificate provisioning, domain management, and integrated monitoring through the Sealos dashboard.
```

### 3. Common Use Cases

List 3-5 practical use cases with brief descriptions:

```markdown
## Common Use Cases

- **[Use Case 1]**: [Brief description]
- **[Use Case 2]**: [Brief description]
- **[Use Case 3]**: [Brief description]
```

### 4. Dependencies and Resources

Document what's included and provide helpful links:

```markdown
## Dependencies for [Application Name] Hosting

The Sealos template includes all required dependencies: [list runtime, databases, storage, etc.].

### Deployment Dependencies

- [Official Documentation](link) - Official documentation
- [Getting Started Guide](link) - Quick start guide
- [Community/Support](link) - Community resources
```

### 5. Implementation Details

Provide technical details about the deployment:

```markdown
### Implementation Details

**Architecture Components:**

This template deploys the following services:

- **[Service 1]**: [Description of primary service]
- **[Service 2]**: [Description of additional service if applicable]
- **[Database]**: [Database details - PostgreSQL/MySQL/MongoDB/Redis]
- **[Object Storage]**: [If applicable - S3-compatible storage details]

**Configuration:**

[Explain key configuration aspects:]
- How components interact
- Scaling considerations
- Default settings

**License Information:**

[Application Name] is licensed under [license type]. [Additional details if relevant]
```

### 6. Why Deploy on Sealos (Platform Benefits)

Highlight Sealos-specific advantages:

```markdown
## Why Deploy [Application Name] on Sealos?

Sealos is an AI-assisted Cloud Operating System built on Kubernetes that unifies the entire application lifecycle, from development in cloud IDEs to production deployment and management. It is perfect for building and scaling modern AI applications, SaaS platforms, and complex microservice architectures. By deploying [Application Name] on Sealos, you get:

- **One-Click Deployment**: Deploy complex applications with a single click. No YAML configuration, no container orchestration complexity - just point, click, and deploy.
- **Auto-Scaling Built-In**: Your applications automatically scale up and down based on demand. Handle traffic spikes without manual intervention or complex configuration.
- **Easy Customization**: Configure environment variables, resource limits, and storage with intuitive forms. Customize your setup without touching a single line of code.
- **Zero Kubernetes Expertise Required**: Get all the benefits of Kubernetes - high availability, service discovery, and container orchestration - without becoming a Kubernetes expert.
- **Persistent Storage Included**: Built-in persistent storage solutions ensure your data is safe and accessible across deployments and scaling events.
- **Instant Public Access**: Each deployment gets an automatic public URL with SSL certificates. Share your applications instantly without complex networking setup.
- **Automated Backups**: Automatic backups and disaster recovery ensure your data is always safe.

Deploy [Application Name] on Sealos and focus on building your product instead of managing infrastructure.
```

### 7. Deployment Guide

Provide step-by-step deployment instructions with strict ordering:

- **Step 1 MUST** start from opening the App Store template page and clicking **Deploy Now**.
- **Do NOT** start deployment steps from Canvas, app cards, or resource cards.
- **Do NOT** validate URL reachability/accessibility (no curl, no browser probing, no HTTP status checks). Write the README directly.
- If the App Store template URL is not explicitly provided, derive it directly from local template metadata (for example `index.yaml`), or use `https://sealos.io/products/app-store/<app-name>` as the default pattern.

```markdown
## Deployment Guide

1. Open the [<Application Name> template](https://sealos.io/products/app-store/<app-name>) and click **Deploy Now**.
2. Configure the parameters in the popup dialog.
3. Wait for deployment to complete (typically 2-3 minutes). After deployment, you will be redirected to the Canvas. For later changes, describe your requirements in the dialog to let AI apply updates, or click the relevant resource cards to modify settings.
4. Access your application via the provided URLs:
   - **[Primary UI]**: Log in with your configured credentials
   - **[API Endpoint]**: For REST or SDK access (if applicable)
```

### 8. Configuration (Optional)

Include if the application requires post-deployment configuration:

```markdown
## Configuration

After deployment, you can configure [Application Name] through:

- **AI Dialog**: Describe the changes you want and let AI apply updates
- **Resource Cards**: Click the relevant resource cards to modify settings
- **Admin Panel**: Access at `https://[your-app-url]/admin`
- **Configuration Files**: [If applicable, explain how to modify config files]
```

### 9. Scaling (Optional)

Include if scaling considerations are important:

```markdown
## Scaling

To scale your application:

1. Open the Canvas for your deployment
2. Click the relevant resource card (Deployment/StatefulSet)
3. Adjust CPU/Memory resources or replica count
4. Apply the changes in the dialog
```

### 10. Troubleshooting (Optional)

Add common issues and solutions if applicable:

```markdown
## Troubleshooting

### Common Issues

**Issue 1: [Common Problem]**
- Cause: [Why this happens]
- Solution: [How to fix]

### Getting Help

- [Official Documentation](link)
- [GitHub Issues](link)
- [Sealos Discord](https://discord.gg/wdUn538zVP)
```

### 11. Additional Resources (Optional)

```markdown
## Additional Resources

- [Application Documentation](link)
- [API Reference](link)
- [Tutorial Videos](link)
- [Example Projects](link)
```

### 12. License

```markdown
## License

This Sealos template is provided under [license]. [Application Name] itself is licensed under [application license].
```

## Bilingual Output

When a bilingual README is required, always write the English README first, then invoke the english-to-chinese-translator skill to produce a Chinese version. Save the Chinese file as README_zh.md and preserve all Markdown structure, code blocks, and URLs.

**Domain Rules:**

- English README: use https://sealos.io for Sealos references
- Chinese README: use https://sealos.run for Sealos references

## Writing Guidelines

### Style and Tone

- **Concise**: Keep paragraphs to 2-3 sentences
- **Professional**: Use clear, technical language without jargon
- **User-Friendly**: Focus on what users need to know
- **Action-Oriented**: Use active voice and clear instructions

### Content Quality

**Must Include:**
- Accurate technical details about architecture
- Clear deployment steps
- Realistic use cases
- Relevant external links (official docs, community resources)

**Must Avoid:**
- Marketing hyperbole or excessive praise
- Assumptions about user knowledge without explanation
- Incomplete or unclear instructions
- Broken or placeholder links
- Deployment guides that begin from Canvas instead of the template page

### Platform-Specific Requirements

When writing for Sealos:

1. **Deployment Entry Order (Mandatory)**: In `Deployment Guide`, Step 1 must be "Open the template page and click Deploy Now"; Canvas appears only after deployment starts/completes
2. **Emphasize One-Click Deployment**: Highlight how Sealos simplifies deployment compared to manual setup
3. **Mention Kubernetes Foundation**: Note that Sealos is built on Kubernetes for credibility
4. **Highlight Cost Benefits**: Mention pay-as-you-go pricing and resource efficiency
5. **Reference Canvas + AI Ops**: For post-deployment changes, mention Canvas, AI dialog, and resource cards; avoid App Launchpad unless required
6. **Sealos Domains by Language**: English README must use https://sealos.io; Chinese README must use https://sealos.run
7. **Standard Deployment Time**: Mention typical deployment takes 2-3 minutes
8. **URL Handling (Mandatory)**: Do not verify URL accessibility. Use URL values from local template metadata directly; if missing, use deterministic URL patterns and continue writing.

### Multi-Service Applications

For applications with multiple components (workers, databases, caches):

1. **Clearly List All Services**: Use bullet points under "Architecture Components"
2. **Explain Interactions**: Describe how services communicate
3. **Document Dependencies**: Note which services depend on others
4. **Include All Provisioned Resources**: Databases, Redis, object storage, etc.

**Example for n8n with workers:**

```markdown
**Architecture Components:**

This template deploys four services:

- **Primary Service**: Main n8n instance serving web UI and API
- **Worker Service**: Background worker processes for workflow execution
- **Redis**: Message broker for job queue management
- **PostgreSQL**: Database for workflow and execution data storage

**Worker Configuration:**

Workers operate independently from the main service, allowing workflow execution to scale horizontally. The Redis queue coordinates job distribution between the main instance and available workers.
```

## Creating a README

To create a README for a new Sealos template:

1. **Gather Information**:
   - Read the template's index.yaml to understand architecture
   - Review the application's official documentation
   - Identify all deployed services (databases, storage, workers)
   - Get the App Store template page URL from local metadata (`index.yaml`, existing README, or template naming convention)
   - If URL is missing, use `https://sealos.io/products/app-store/<app-name>` directly
   - Do not validate URL accessibility before writing
   - Note key features and use cases

2. **Follow the Structure**: Use the sections outlined above in order

3. **Customize Content**:
   - Replace all `[Application Name]` placeholders
   - Fill in architecture details from index.yaml
   - Add realistic use cases for the specific application
   - Include relevant external links

4. **Generate Chinese README** (if required):
   - Invoke the english-to-chinese-translator skill after the English README is complete
   - Preserve Markdown structure, code blocks, and URLs
   - Save the output as README_zh.md

5. **Verify Accuracy**:
   - Ensure all service names match the template
   - Confirm `Deployment Guide` Step 1 opens the App Store template page and clicks **Deploy Now**
   - Confirm deployment instructions do not begin from Canvas
   - Confirm Canvas/AI dialog/resource cards are described only as post-deployment operations
   - Confirm URL/domain format follows skill rules (no accessibility checks required)
   - Check that technical details align with index.yaml

6. **Review for Quality**:
   - Read through for clarity and completeness
   - Ensure consistent formatting
   - Check for typos and grammar
   - Verify all sections are filled appropriately

## Examples

### Simple Single-Service Application (Typesense)

```markdown
# Deploy and Host Typesense on Sealos

Typesense is a fast, typo-tolerant search engine optimized for instant search experiences. This template deploys a production-ready Typesense instance with persistent storage on Sealos Cloud.

## About Hosting Typesense

Typesense runs as a single-node search engine service that provides instant search results with typo tolerance and faceting capabilities. The Sealos template automatically provisions persistent storage for your search indices and data, ensuring your search data is safely stored and survives restarts.

## Common Use Cases

- **E-commerce Search**: Fast product search with typo tolerance and filtering
- **Documentation Search**: Instant search across documentation sites
- **Log Search**: Quick log analysis and searching
```

### Multi-Service Application (n8n)

```markdown
# Deploy and Host n8n (w/ workers) on Sealos

n8n is a workflow automation tool that uses a node-based approach to connect services and automate processes. This template deploys n8n with a worker architecture for handling workflow execution at scale.

## About Hosting n8n (w/ workers)

n8n (w/ workers) runs as a multi-service architecture where the main instance handles the web interface and API while worker processes execute workflows. The main service manages workflow definitions, user authentication, and the web UI, while workers pull jobs from a Redis queue to execute workflows independently. The Sealos template automatically provisions and configures Redis for job queuing and PostgreSQL for workflow storage.

**Architecture Components:**

This template deploys four services:

- **Primary Service**: Main n8n instance serving web UI and API
- **Worker Service**: Background worker processes for workflow execution
- **Redis**: Message broker for job queue management
- **PostgreSQL**: Database for workflow and execution data storage
```

## Reference Materials

For detailed Sealos template specifications, consult the reference file which contains comprehensive information about template structure, resource ordering, configuration requirements, and platform-specific constraints.

Load `references/sealos-template-specs.md` when you need detailed information about:
- Template file organization and naming conventions
- Resource creation order requirements
- Database and storage configuration
- ConfigMap and volume mount specifications
- Environment variable and service discovery rules
- Labels and metadata requirements
- Platform-specific constraints and limitations
