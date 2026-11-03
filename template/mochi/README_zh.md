# Mochi

一个住在 **Discord、Telegram、Slack、QQ 和 LINE** 里的 AI 机器人 —— 带控制台、长期记忆、可上传的知识库，以及一个网页挂件。

一个 Flatkey 密钥就能覆盖她需要的所有模型（对话、视觉、联网搜索、记忆）。

## 你会得到什么

- **五个渠道**：Discord（WebSocket）、Telegram（长轮询）、Slack（Socket Mode）、QQ（官方机器人）、LINE（webhook —— 需要公网 HTTPS 地址，Sealos 正好提供）。
- **控制台**：`https://<你的域名>/dashboard/`，用部署时设置的 `admin_token` 解锁。
- **记忆与知识库**：她记得每个人、每个群聊之前说过什么，也能根据你上传的文档（PDF/Word/Markdown/网页）回答，支持中、英、日、葡四种语言。
- **网页挂件**：一行 `<script>` 就能挂到你自己的网站上。
- **数据在你手里**：机器人配置、记忆、知识库、渠道令牌全部存在应用的存储卷（`/app/data`）里，不会发给我们。

## 部署之后

1. 打开应用页上的控制台地址，用 `admin_token` 解锁。
2. **Flatkey API key** → 粘贴你的密钥。没有就去 [console.flatkey.ai/keys](https://console.flatkey.ai/keys?utm_source=mochi_bot&utm_medium=app_store&utm_campaign=mochi&utm_content=sealos_template_zh) 创建。
3. **Bots → 你的机器人 → Channels** → 连接你要的平台：
   - **Discord**：粘贴 bot token，控制台会给出邀请链接。
   - **Telegram**：粘贴 @BotFather 给的 token。
   - **Slack**：把控制台生成的 manifest 贴进去，再填两个 token。
   - **QQ**：q.qq.com 的 AppID + AppSecret。
   - **LINE**：channel access token + channel secret，然后把 webhook 设成
     `https://<你的域名>/webhook/line/mochi`，并打开 **Use webhook**。
4. 可选：**知识库** → 上传你的 FAQ 或产品文档；如果访客说多种语言，打开「上传时翻译成所有语言」。

## 注意事项

- **只跑一个副本**：同一个 Telegram token 只能有一个进程轮询，SQLite 也要拿写锁，两个 pod 会互相打架。
- 存储卷里是全部数据 —— 除非想从头开始，别删。
- 源码、问题反馈和自托管说明：[AM-young-fun/Mochi-ai-chatbot](https://github.com/AM-young-fun/Mochi-ai-chatbot)。
