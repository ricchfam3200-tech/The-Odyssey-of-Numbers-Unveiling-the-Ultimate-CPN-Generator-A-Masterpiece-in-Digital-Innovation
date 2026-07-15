# Profile Number Generator

Generates random 9-digit numbers that pass a Luhn check digit validation, with a small Flask web
front end for on-demand generation and a standalone CLI script (`main.py`) for batch generation.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Then visit `http://localhost:5000`.

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

No environment variables are required to run. Optional overrides:

- `MIN_PROFILE_NUMBER` / `MAX_PROFILE_NUMBER` — bounds for generated numbers (see `config/settings.py`).
