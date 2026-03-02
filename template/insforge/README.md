# InsForge

**InsForge is the backend built for AI-assisted development.**
Connect InsForge with any agent. Add authentication, database, storage, functions, and AI integrations to your app in seconds.
## Key Features & Use Cases

### Core Features:
- **Authentication** - Complete user management system
- **Database** - Flexible data storage and retrieval
- **Storage** - File management and organization
- **AI Integration** - Chat completions and image generation (OpenAI-compatible)
- **Serverless Functions** - Scalable compute power
- **Site Deployment** *(coming soon)* - Easy application deployment

### Use Cases: Building full-stack applications using natural language
- **Connect AI agents to InsForge** - Enable Claude, GPT, or other AI agents to manage your backend

## Prompt Examples:

<td align="center">
  <img src="https://raw.githubusercontent.com/InsForge/InsForge/main/assets/userflow.png" alt="userFlow">
  <br>
</td>

## Quickstart TLDR;

### 0. Deploy on Sealos Cloud

[![Deploy on Sealos](https://raw.githubusercontent.com/labring-actions/templates/main/Deploy-on-Sealos.svg)](https://template.hzh.sealos.run/deploy?templateName=insforge)

### 1. Connect an AI Agent

Visit InsForge Dashboard (default: https://[appname].usw-1.sealos.app), log in, and follow the "Connect" guide, and set up your MCP.

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://raw.githubusercontent.com/InsForge/InsForge/main/assets/signin.png" alt="Sign In">
        <br>
        <em>Sign in to InsForge</em>
      </td>
      <td align="center">
        <img src="https://raw.githubusercontent.com/InsForge/InsForge/main/assets/mcpInstallv2.png" alt="MCP Configuration">
        <br>
        <em>Configure MCP connection</em>
      </td>
    </tr>
  </table>
</div>

### 2. Test the Connection

In your agent, send:
```
I'm using InsForge as my backend platform, fetch InsForge instruction doc to learn more about InsForge.
```

<div align="center">
  <img src="https://raw.githubusercontent.com/InsForge/InsForge/main/assets/sampleResponse.png" alt="Successful Connection Response" width="600">
  <br>
  <em>Sample successful response calling insforge MCP tools</em>
</div>

### 3. Start Using InsForge

Start building your project in a new directory! Build your next todo app, Instagram clone, or online platform in seconds!

**Sample Project Prompt:**

"Build an app similar to Reddit with community-based discussion threads using InsForge as the backend platform that has these features:
- Has a "Communities" list where users can browse or create communities
- Each community has its own posts feed
- Users can create posts with a title and body (text or image upload to InsForge storage)
- Users can comment on posts and reply to other comments
- Allows upvoting and downvoting for both posts and comments
- Shows vote counts and comment counts for each post"

## Architecture

```mermaid
graph TD
    subgraph agents[" "]
        A1[Claude]
        A2[Cursor]
        A3[Windsurf]
        A4[Coding Agent]
    end

    A1 --> MCP[Model Context Protocol]
    A2 --> MCP
    A3 --> MCP
    A4 --> MCP

    MCP -->|fetch-docs| INS[InsForge Instructions]

    MCP -->|create-bucket| S[Storage]
    MCP --> AUTH[Auth]
    MCP -->|run-raw-sql| DB[Database]
    MCP -->|create-function| EF[Edge Function]
    MCP --> AI[AI Integration]

    style agents fill:#1a1a1a,stroke:#666,color:#fff
    style MCP fill:#000,stroke:#666,color:#fff
    style INS fill:#4a5568,stroke:#666,color:#fff
    style S fill:#4a5568,stroke:#666,color:#fff
    style AUTH fill:#4a5568,stroke:#666,color:#fff
    style DB fill:#4a5568,stroke:#666,color:#fff
    style EF fill:#4a5568,stroke:#666,color:#fff
    style AI fill:#4a5568,stroke:#666,color:#fff
    style A1 fill:#4a5568,stroke:#666,color:#fff
    style A2 fill:#4a5568,stroke:#666,color:#fff
    style A3 fill:#4a5568,stroke:#666,color:#fff
    style A4 fill:#4a5568,stroke:#666,color:#fff
```
