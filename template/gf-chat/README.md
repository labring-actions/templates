# GF Chat

An AI girlfriend chat application with long-term memory. Pick a name and
personality, talk every day, and the relationship grows: she remembers what you
told her, keeps a diary, and sometimes messages you first.

## Features

- **Multiple personalities**: gentle, tsundere, aloof, sharp, grumpy, shy
- **Long-term memory**: preferences, corrections and events are extracted in the
  background and re-used in later conversations; outdated memories are replaced
- **Lightweight RAG**: uploaded notes are chunked and retrieved with BM25
- **Intimacy system**: six levels that change how she addresses and talks to you
- **Proactive messages**: she starts the conversation after long silences
- **Diary and timeline**: one diary entry per day, plus a "how she sees you" profile
- **Voice**: Doubao TTS playback and voice calls with automatic silence detection
- **Persistent data**: memories, diaries and intimacy are stored in `/app/data`

## Deploy on Sealos

1. Click **Deploy** on this template.
2. Fill in the inputs below.
3. Open the assigned domain and set her name and personality.

### Inputs

| Input | Required | Description |
|---|---|---|
| `deepseek_api_key` | Yes | DeepSeek API key, used as the main chat model |
| `access_password` | No | Password required to open the page; leave empty to disable login |
| `volc_api_key` | No | Volcengine speech key for TTS and voice calls; falls back to browser speech |
| `bigmodel_api_key_1` | No | Zhipu API key for memory extraction and the Flash fallback model |
| `bigmodel_api_key_2` | No | Zhipu API key for the GLM Pro fallback model |

## Data persistence

The template mounts a 1 GiB volume at `/app/data`. Memories, diaries, intimacy
scores and cache files survive pod restarts and redeploys.

## Notes

- The container listens on port `8000`; the public domain is created by the Ingress.
- Photo generation depends on the `dreamina-canvas` CLI, which is not bundled in
  the image, so the camera button is hidden automatically.
- Model routing: DeepSeek is the primary path, GLM models are used as fallbacks.

## Links

- Source code: https://github.com/Lijian2004/gf-chat
