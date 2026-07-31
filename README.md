# Kuchu Puchu Video Automation

Free, fully automated pipeline: script → image → voice → video → YouTube upload.
Runs on GitHub Actions (free compute, real internet access, no card needed).

## Setup (one-time, ~10 min)

1. **Create a new GitHub repo**, push this folder into it.

2. **Get a free Groq API key**: https://console.groq.com → API Keys → create.

3. **Get YouTube upload credentials** (one-time, do this on your own PC):
   - Go to Google Cloud Console → create project → enable "YouTube Data API v3"
   - Create OAuth 2.0 Client ID (Desktop app) → download client_secret.json
   - Run a small local script (ask me for it) once to get YT_REFRESH_TOKEN

4. **Add these as GitHub repo secrets** (Settings → Secrets and variables → Actions):
   - `GROQ_API_KEY`
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`

5. **Test it**: Go to Actions tab → "Kuchu Puchu Video Automation" → Run workflow (manual button).
   Video will also appear as a downloadable artifact even before upload, so you can check it first.

## Notes
- Runs daily automatically (9 AM UTC) once secrets are set — no manual work needed after setup.
- Pollinations.ai image gen + edge-TTS voice are both free with no API key.
- To change style, edit the `scene_prompt` instructions inside `scripts/generate_content.py`.
