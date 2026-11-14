# YouTube Shorts Automation

A zero-subscription, cloud-run starter for a daily vertical Shorts channel covering **GTA 6** and **original animated micro-stories**.

## What this version does

- Runs in GitHub Actions (no computer needs to stay on).
- Alternates between GTA 6 explainers and original short stories.
- Uses a curated, editable fact bank for GTA 6. It does **not** invent breaking news or claim rumours are confirmed.
- Generates narration with the runner's local `espeak-ng` voice and renders a vertical 1080x1920 video with animated text cards using Pillow + FFmpeg.
- Uploads through the YouTube Data API using OAuth refresh-token credentials.
- Keeps a history file to avoid repeating topics.
- Defaults to **private test uploads** until you deliberately enable publishing.

## Important constraints

This is a practical no-paid-API baseline, not a promise of studio-quality generative animation. GitHub-hosted runners are temporary and are not suitable for running large AI video models. The first version uses original motion-graphic scenes and synthetic narration. Better voices or AI-generated images can be added later if a genuinely free, reliable provider is selected.

YouTube Data API projects that have not passed the required audit may be restricted to private uploads. The code therefore supports private test mode and scheduled publishing, but publishing is not guaranteed until Google's API project is eligible. Never put OAuth credentials in the repository.

## Repository setup

1. In GitHub, open **Settings → Secrets and variables → Actions**.
2. Add these repository secrets:
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN`
3. The refresh token must be generated for the same Google account that owns/manages the target YouTube channel and must include the YouTube upload scope.
4. Set repository variable `YOUTUBE_CHANNEL_ID` only if you want the workflow to sanity-check the expected channel.
5. Keep `PUBLISH_PUBLIC` unset or `false` for initial tests. Set it to `true` only after checking several generated videos and confirming your API project can publish.
6. In **Settings → Actions → General**, allow GitHub Actions to read and write repository contents so it can commit `storage/history.json`.

## Run manually

Actions → Daily Shorts → Run workflow.

The scheduled run starts at 13:00 UTC (18:30 India time) to leave time for rendering and upload before the 19:00 India target. GitHub scheduled workflows can be delayed, so 7 PM is a target, not a guaranteed exact delivery time.

## Local development

Python 3.11+, FFmpeg and espeak-ng are required.

```bash
python -m pip install -r requirements.txt
python main.py --dry-run
```

A dry run creates a video in `output/` and does not contact YouTube.

## Content safety

- GTA 6 scripts must be based on the checked-in fact bank and cite the source URL in the description.
- Rumours/theories are explicitly labelled as speculation.
- No leaked footage, copyrighted gameplay clips, copied scripts, fabricated release updates, or impersonation.
- Story scripts are original text generated from local story structures.
- Review platform rules on synthetic/altered content and monetization before enabling public uploads.
