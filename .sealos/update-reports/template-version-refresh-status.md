# Sealos Template Version Refresh Status

Generated: 2026-06-24T13:10:47.133772+00:00

## Selection Policy

Start with patch-level application image candidates, then ship only candidates whose focused docker-to-sealos validation can pass with image-refresh-scoped edits.

## Updated Candidates

| Template | Current image | Candidate image | Status | Evidence |
|---|---|---|---|---|
| pdf2zh | `byaidu/pdf2zh:1.9.6` | `byaidu/pdf2zh:1.9.11` | updated | crane ls |

## Skipped Candidates

| Template | Candidate image | Reason |
|---|---|---|
| affine | `ghcr.io/toeverything/affine:0.26.7` | Skipped from this PR because focused docker-to-sealos validation found 4 existing template issues outside the image-refresh scope. |
| cronicle | `soulteary/cronicle:0.9.80` | Skipped from this PR because focused docker-to-sealos validation found 9 existing template issues outside the image-refresh scope. |
| illa-builder | `illasoft/illa-builder:v4.8.5` | Skipped from this PR because focused docker-to-sealos validation found 10 existing template issues outside the image-refresh scope. |
| kanboard | `kanboard/kanboard:v1.2.52` | Skipped from this PR because focused docker-to-sealos validation found 4 existing template issues outside the image-refresh scope. |
| lobe-chat-db | `lobehub/lobe-chat-database:1.143.3` | Skipped from this PR because focused docker-to-sealos validation found 8 existing template issues outside the image-refresh scope. |
| outline | `outlinewiki/outline:1.8.2-0` | Skipped from this PR because focused docker-to-sealos validation found 8 existing template issues outside the image-refresh scope. |
| pageplug | `cloudtogouser/pageplug-ce:v1.9.37` | Skipped from this PR because focused docker-to-sealos validation found 9 existing template issues outside the image-refresh scope. |
| presenton | `ghcr.io/presenton/presenton:v0.8.9-beta` | Skipped from this PR because focused docker-to-sealos validation found 3 existing template issues outside the image-refresh scope. |
| stalwart | `stalwartlabs/stalwart:v0.16.10` | Skipped from this PR because focused docker-to-sealos validation found 8 existing template issues outside the image-refresh scope. |
| sub2api | `weishaw/sub2api:0.1.138` | Skipped from this PR because focused docker-to-sealos validation found 5 existing template issues outside the image-refresh scope. |
| tailchat | `moonrailgun/tailchat:1.11.11` | Skipped from this PR because focused docker-to-sealos validation found 22 existing template issues outside the image-refresh scope. |
| tududi | `chrisvel/tududi:1.1.1` | Skipped from this PR because focused docker-to-sealos validation found 4 existing template issues outside the image-refresh scope. |
| webos | `fs185085781/webos:v1.4.4` | Skipped from this PR because focused docker-to-sealos validation found 6 existing template issues outside the image-refresh scope. |

## Validation Notes

- Repository scripts/check_consistency.py and scripts/quality_gate.py are not present in this checkout.
- docker-to-sealos self-tests passed.
- Focused docker-to-sealos validation passes for template/pdf2zh/index.yaml after the scoped Service metadata fix.
