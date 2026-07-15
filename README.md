# Profile Number Generator

Generates random 9-digit numbers that pass a Luhn check digit validation, with a small Flask web
front end for on-demand generation, a Telegram bot for the same flow, and a standalone CLI script
(`main.py`) for batch generation.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Then visit `http://localhost:5000`.

## Setting up the Telegram bot

`telegram_bot.py` is a standalone script that long-polls Telegram for new messages — no public URL
or webhook registration required, so it doesn't depend on your web host supporting background
processes.

### Running it on Replit (recommended)

1. Import this repo into a new Repl.
2. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token it gives you.
3. In the Repl, open **Secrets** (the padlock icon) and add:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: your token
4. Click **Run** — `.replit` is already set up to launch `telegram_bot.py`.
5. Message your bot on Telegram and send `/start` to walk through name, state, and date of birth,
   then get back a generated profile number.
6. For the bot to keep responding when you're not actively viewing the Repl, turn on **Always On**
   (or use a Reserved VM Deployment) in the Repl's settings — otherwise it only runs while the tab
   is open.

### Running it anywhere else

```bash
export TELEGRAM_BOT_TOKEN="your-token-here"
python telegram_bot.py
```

Any host that can keep a long-running Python process alive works (a VPS, your own machine, etc.).
This does not need to be the same host as the Flask web app.

## Deploying to Render

This repo includes a `render.yaml` Blueprint, so Render can configure the service automatically:

1. Push this repo to GitHub (already done if you're reading this on the deploy branch).
2. In the Render dashboard, click **New +** -> **Blueprint**.
3. Connect this repository. Render will detect `render.yaml` and pre-fill the service
   (Python web service, `pip install -r requirements.txt`, `gunicorn app:app`).
4. Click **Apply** to create and deploy the service.

If you'd rather configure it by hand instead of using the Blueprint, create a **Web Service** with:

- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

No environment variables are required to run the web service. Optional overrides:

- `MIN_PROFILE_NUMBER` / `MAX_PROFILE_NUMBER` — bounds for generated numbers (see `config/settings.py`).

The Telegram bot (`telegram_bot.py`) is a separate process, not part of this web service — see
"Setting up the Telegram bot" above.
