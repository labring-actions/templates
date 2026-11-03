# Mochi

An AI chatbot that lives in **Discord, Telegram, Slack, QQ and LINE** — with a dashboard, long-term memory, a knowledge base you can upload to, and a website widget.

One Flatkey key covers every model she needs (chat, vision, web search, memory).

## What you get

- **Five channels**: Discord (WebSocket), Telegram (polling), Slack (Socket Mode), QQ (official bot), LINE (webhook — needs a public HTTPS address, which Sealos gives you).
- **Dashboard** at `https://<your domain>/dashboard/` — the password is the `admin_token` you set when deploying.
- **Memory and knowledge**: she remembers people and rooms between conversations, and answers from documents you upload (PDF/Word/Markdown/URL), in English, Chinese, Portuguese and Japanese.
- **Website widget**: one `<script>` tag for your own site.
- **Your data stays yours**: everything lives in the application's volume (`/app/data`) — bots, memory, knowledge, channel tokens. Nothing is sent to us.

## After deploying

1. Open the dashboard URL shown on the app page, and unlock it with your `admin_token`.
2. **Flatkey API key** → paste your key. Create one at [console.flatkey.ai/keys](https://console.flatkey.ai/keys?utm_source=mochi_bot&utm_medium=app_store&utm_campaign=mochi&utm_content=sealos_template).
3. **Bots → your bot → Channels** → connect the platforms you want:
   - **Discord**: paste the bot token; the dashboard shows the invite link.
   - **Telegram**: paste the token from @BotFather.
   - **Slack**: paste the manifest the dashboard gives you, then the two tokens.
   - **QQ**: AppID + AppSecret from q.qq.com.
   - **LINE**: channel access token + channel secret, then set the webhook to
     `https://<your domain>/webhook/line/mochi` and turn on **Use webhook**.
4. Optional: **Knowledge** → upload your FAQ or product docs, and turn on *Translate uploads into every language* if your visitors speak several.

## Notes

- **Keep one replica.** A Telegram bot token can only be polled by one process, and the SQLite database takes a write lock; two pods would conflict.
- The volume holds everything that matters — do not delete it unless you want a fresh start.
- Source, issues and self-hosting guides: [AM-young-fun/Mochi-ai-chatbot](https://github.com/AM-young-fun/Mochi-ai-chatbot).
