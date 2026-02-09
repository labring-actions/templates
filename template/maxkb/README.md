# MaxKB Sealos 模板

## 简介

MaxKB 是一款基于 LLM 大语言模型的知识库问答系统。MaxKB = Max Knowledge Base，旨在成为企业的最强知识库。

## 功能特点

- 支持多种文档格式：PDF、Word、Excel、PPT、TXT、Markdown 等
- 支持多种大语言模型：OpenAI、Azure OpenAI、智谱 AI、通义千问等
- 提供开箱即用的数据处理、模型调用等能力
- 支持知识库管理和问答交互
- 提供 API 接口供第三方系统集成

## 部署配置

### 资源配置

- CPU: 500m (请求) / 2000m (限制)
- 内存: 1Gi (请求) / 4Gi (限制)
- 存储: 5Gi (持久化存储)

### 端口说明

- 8080: Web 界面和 API 接口

### 存储说明

- `/opt/maxkb`: 应用数据目录，包含数据库、文件上传、配置等

## 使用说明

1. 部署完成后，通过外网地址访问 MaxKB Web 界面
2. 首次访问会进入初始化设置页面
3. 配置大语言模型 API 密钥
4. 创建知识库并上传文档
5. 开始使用知识库问答功能

## 注意事项

- MaxKB 需要配置大语言模型 API 才能正常工作
- 建议根据实际使用情况调整资源配置
- 持久化数据存储在 /opt/maxkb 目录，确保不会丢失

## 相关链接

- 官方网站: https://github.com/1Panel-dev/MaxKB
- 文档: https://maxkb.cn
