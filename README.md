# X Content Agent — free-tier MVP

Generates a diverse daily batch of X drafts from your persona and curated RSS feeds. Uses Gemini and Buffer's free API. **No X API key required.** The default workflow previews only.

## Setup

1. Create a free Buffer account and connect your X profile: https://buffer.com/pricing
2. Get your Buffer API key: https://publish.buffer.com/settings/api (API settings in your account)
3. Create a Gemini API key: https://aistudio.google.com/apikey (check current free-tier eligibility/limits).
4. Install Python 3.11+, then:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

5. Put the Gemini and Buffer keys into `.env`. **Never commit `.env`**.
6. Replace the placeholder `persona.md` with your own posts and preferences.
7. Run `python daily_agent.py --count 5` to preview five varied drafts. No post is published.
8. Run `python agent.py --list-channels`, copy your X channel ID into `.env` as `BUFFER_CHANNEL_ID`.
9. When happy with the draft quality, run `python daily_agent.py --count 5 --queue` to schedule up to five posts at Buffer's next free slots. This actually creates queued posts. It checks Buffer's existing 10-slot free queue and the current day's successful submissions first.

Optional: Create `today.md` (see `today.md.example`) with real recent activities. This is required if you want the agent to say you personally learned, built or did something that day. Don't commit private details.

## GitHub Actions

Push the **contents** of this folder as a GitHub repository. In repository Settings → Secrets and variables → Actions, add `GEMINI_API_KEY`, `BUFFER_API_KEY`, `BUFFER_CHANNEL_ID` as **secrets**. Optionally add `PRIVATE_DATA_TOKEN` if you want the workflow to read/write a separate private `puravky/x-agent-data` repository for persona/history persistence. Without `PRIVATE_DATA_TOKEN`, the workflow uses local `app/data` state only. The included workflow runs daily at about 09:00 IST (03:30 UTC), and **generates previews only** by default. After checking drafts and configuring five spaced-out daily posting slots in Buffer, add repository **variable** `ENABLE_AUTO_QUEUE=true` to enable queueing. The workflow commits `data/daily_state.json` back into the repository so duplicate checking and same-day idempotency survive fresh runners. Keep the repository private if you don't want draft history public. The default GitHub Actions token needs permission to push commits; check repository Actions workflow permissions if this fails.

If you run locally with `--queue`, commit `data/daily_state.json` before allowing GitHub Actions to queue posts, so both environments know what's already scheduled. Do not run parallel local and hosted queueing jobs.

## Limitations & safety

- RSS topic titles are *inspiration*, not verified evidence; generated posts should be reviewed for accuracy.
- This MVP does not read your X connections. Doing that automatically requires permitted X data access. You can add manually curated inputs later.
- The writing style is based on posts you provide; no automatic profile scraping.
- The daily job targets five varied posts, but queue capacity, validation failures and API limits can reduce that day's total. The free Buffer queue holds 10 scheduled posts at a time, not 10 total per month.
- Automatic posting has operational risks. Review a few batches before enabling it, and periodically check Buffer for errors or low-quality posts. A semantic duplicate check and claim verification by a human remain better than the built-in heuristics.
- Free allowances and model availability change. Set `GEMINI_MODEL` to a model available to your account.
- Buffer free queue: 10 scheduled posts per channel; it refills as posts publish. Respect X automation rules, avoid duplicates and spam.
