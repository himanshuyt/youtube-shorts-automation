# YouTube Shorts Automation

A zero-subscription, cloud-run starter for one daily YouTube Short covering **GTA 6** and **original short stories**.

## Current implementation

- GitHub Actions runs in the cloud; no personal computer needs to stay on.
- Alternates GTA 6 explainers and original short stories.
- GTA 6 scripts use a small checked-in fact bank and include source links. The starter does not fetch breaking news or invent new facts.
- Narration uses the runner's local `espeak-ng` voice.
- Pillow + FFmpeg render a vertical 1080x1920 video from original text-card scenes.
- YouTube uploads use OAuth refresh-token credentials.
- A JSON history tracks used topics and successful uploads.
- Manual workflow runs default to a safe video-only dry run.

## Honest limitations

This is a working starter, not a finished AI animation studio. The current renderer creates designed text-card scenes with synthetic narration; it does **not** yet generate moving character animation or AI images. The scripts are generated from local templates/seeds, not a cloud LLM. Large AI video models are not practical on standard free GitHub runners. A genuinely free and reliable AI animation provider would need to be added and tested separately.

Google may restrict uploads from unaudited YouTube API projects to private visibility. Public scheduled publishing is therefore not guaranteed until the Google API project is eligible. GitHub scheduled workflows can also start late, so 7 PM IST is a target rather than an exact guarantee.

## One-time setup

1. Open **Settings → Secrets and variables → Actions** in this repository.
2. Add these repository secrets:
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN`
3. Generate the refresh token for the Google account that manages the target YouTube channel, with the `youtube.upload` scope. Never commit credentials or paste them into source files.
4. For private test uploads, leave the repository variable `SCHEDULE_PUBLIC` unset or set it to `false`.
5. Only after private upload testing and confirming YouTube API eligibility, set `SCHEDULE_PUBLIC` to `true`. The uploader will upload privately with a scheduled publish time of 7 PM India time.
6. In **Settings → Actions → General**, allow GitHub Actions to read and write repository contents so it can commit `storage/history.json`.

## Test the video renderer

1. Open **Actions → Daily Shorts → Run workflow**.
2. Keep `dry_run` enabled.
3. Download the `shorts-dry-run` artifact from the completed run. It contains the rendered MP4.
4. Check the voice, spelling, pacing, visuals and duration before enabling uploads.

## Schedule

The daily workflow starts at 13:00 UTC (18:30 India time), leaving time to render and upload before the 19:00 India target. GitHub may delay scheduled runs.

## Local development

Requires Python 3.11+, FFmpeg and espeak-ng.

```bash
python -m pip install -r requirements.txt
python main.py --dry-run
```

## Content rules

- Use official sources for GTA 6 facts; label theories as speculation.
- No leaks, fabricated updates, copied scripts, unauthorized gameplay footage or impersonation.
- Story scripts are fictional and original to this project.
- Review YouTube rules on synthetic/altered content and monetization before public publishing.
