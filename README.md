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

## Running the Telegram bot locally

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token it gives you.
2. Set it as an environment variable (don't commit it to the repo):
   ```bash
   export TELEGRAM_BOT_TOKEN="your-token-here"
   ```
3. Run the bot:
   ```bash
   python telegram_bot.py
   ```
4. Message your bot on Telegram and send `/start` to walk through name, state, and date of birth,
   then get back a generated profile number.

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

The Blueprint also defines a **Background Worker** for the Telegram bot
(`profile-number-generator-bot`), running `python telegram_bot.py`. It requires one environment
variable, set in the Render dashboard (not in `render.yaml`, so the token stays out of the repo):

- `TELEGRAM_BOT_TOKEN` — the token from @BotFather.
