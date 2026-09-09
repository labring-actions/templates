# Deploy and Host MoneyPrinterTurbo on Sealos

MoneyPrinterTurbo turns a topic or script into a short video with footage, narration, subtitles, and background music. This template runs the official v1.3.6 WebUI with persistent configuration and video storage on Sealos.

![MoneyPrinterTurbo project screenshot](https://raw.githubusercontent.com/labring-actions/templates/kb-0.9/template/moneyprinterturbo/website-screenshot.webp)

## About Hosting MoneyPrinterTurbo

The Streamlit WebUI provides controls for script generation, material selection, voiceover, subtitles, and video export. Cloud providers supply optional AI services, while FFmpeg processes and combines videos inside the application container.

Sealos provisions one application instance, a persistent volume, and an HTTPS address. Saved settings, uploaded materials, and generated files share persistent storage and survive Pod replacement. The application uses shared, single-user settings.

## Common Use Cases

- **Short social videos**: Combine scripts, stock footage, narration, and captions.
- **Local video editing**: Upload your own clips and select framing, transitions, and audio options.
- **Multilingual content**: Choose supported text and voice providers for different languages.
- **Repeatable video styles**: Export and import generation presets through the WebUI.

## Dependencies for MoneyPrinterTurbo Hosting

The official image includes Python, Streamlit, FFmpeg, fonts, and application dependencies. Cloud script generation and online material providers require their own API keys, configured after deployment.

### Deployment Dependencies

- [Official English documentation](https://github.com/harry0703/MoneyPrinterTurbo/blob/v1.3.6/README-en.md)
- [Configuration reference](https://github.com/harry0703/MoneyPrinterTurbo/blob/v1.3.6/config.example.toml)
- [Release notes](https://github.com/harry0703/MoneyPrinterTurbo/releases/tag/v1.3.6)
- [Community support](https://github.com/harry0703/MoneyPrinterTurbo/issues)

### Implementation Details

| Component | Configuration |
| --- | --- |
| Application | One StatefulSet replica using `ghcr.io/harry0703/moneyprinterturbo:v1.3.6` |
| Web entry | Streamlit on port 8501, exposed through HTTPS |
| Application resources | Limits: 4 CPU, 4096Mi RAM; requests: 400m CPU, 409Mi RAM |
| Configuration initialization | Limits: 100m CPU, 128Mi RAM; requests: 10m CPU, 12Mi RAM |
| Persistent storage | One 1Gi volume mounted at `/MoneyPrinterTurbo/storage` |
| Saved configuration | `/MoneyPrinterTurbo/storage/config.toml`, loaded through `/MoneyPrinterTurbo/config.toml` |

The resource limits follow the upstream minimum of 4 CPU cores and 4 GB RAM. Live validation covered cold startup, settings changes, local material upload, and a 1080×1920 video render. Larger videos, batch jobs, or local Whisper models need additional capacity; increase storage before downloading large models.

This template preserves the existing WebUI-only topology. Its storage backend is the local filesystem; optional Redis task state and the separate upstream API service remain outside this deployment.

MoneyPrinterTurbo is licensed under the MIT License.

## Why Deploy MoneyPrinterTurbo on Sealos?

Sealos provides a Kubernetes foundation with one-click deployment, managed HTTPS, persistent storage, and resource monitoring. Pay-as-you-go billing and adjustable resource limits let you match capacity to your workload. After deployment, use the Canvas AI dialog or resource cards to manage the application.

## Deployment Guide

1. Open the [MoneyPrinterTurbo template](https://sealos.io/products/app-store/moneyprinterturbo) and click **Deploy Now**.
2. Review the application resources and deploy. Configure provider API keys in the WebUI after startup.
3. Wait for deployment to finish, typically 2-3 minutes; the first image pull may take longer. Open the deployment Canvas and use the application's public URL.
4. The WebUI opens directly. **This release has no built-in WebUI registration or login.** Anyone who can reach the URL can operate the application and its shared settings. Restrict access to trusted users before entering provider credentials.
5. Use **Language / 语言** to choose your language. Open **Settings** or **Configure AI model** to configure a provider and its API key; configure online footage credentials through **Configure material sources**.
6. Enter a topic or script, choose your video and audio options, and click **Generate Video**. When processing finishes, preview the result and click **Download Video**.

### Try a Local Video

For a provider-independent check, upload a clip at least 480×480 pixels using **Video Source → Local file**, enter a script, select **Voiceover Mode → None** and **No Background Music**, and clear **Enable Subtitles**. Click **Generate Video** and download the result. A 3-second 640×640 test clip was successfully rendered as a portrait 1080×1920 video.

## Configuration and Storage

Settings are saved automatically. The initialization container copies the official example only when the persistent configuration file is absent. The launcher places configuration temporary files on the same volume as the saved file so updates remain atomic.

Use **Settings Preset** to export or import video settings. Provider credentials can be backed up through **Settings → Key Backup**; keep exported key files private. Download videos you want to retain and manage the 1Gi storage allocation through the Canvas resource card.

For an existing deployment using the older volume claim name, back up configuration and video data before adopting this template. The normalized claim name creates a different PVC; transfer the backup to the new deployment and verify it before removing the old storage.

## Troubleshooting

- **Provider credentials requested**: Configure the selected cloud service in Settings, or use the local-video workflow above.
- **Local footage rejected**: Supply valid video files with both dimensions at least 480 pixels.
- **Large uploads rejected**: The Ingress accepts requests up to 32 MB. Increase its body-size limit for larger uploads and check Streamlit's upload-size setting.
- **Slow rendering or full storage**: Inspect the resource cards and logs in Canvas. Increase CPU, RAM, or disk for longer videos and local transcription models.

## License

MoneyPrinterTurbo is distributed under the [MIT License](https://github.com/harry0703/MoneyPrinterTurbo/blob/v1.3.6/LICENSE). This template follows the licensing terms of the Sealos templates repository.
