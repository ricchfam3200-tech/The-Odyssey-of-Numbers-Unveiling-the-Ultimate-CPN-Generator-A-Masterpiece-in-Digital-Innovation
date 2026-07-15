import logging
import os

from flask import Flask, jsonify, render_template_string

from luhn_algorithm import calculate_luhn_check_digit
from main import ProfileNumberGenerator
from utils import is_valid_number

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/profile_number_generator.log", level=logging.INFO)

app = Flask(__name__)
profile_number_generator = ProfileNumberGenerator()

INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Profile Number Generator</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 640px; margin: 4rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { font-size: 1.5rem; }
    button { font-size: 1rem; padding: 0.6rem 1.2rem; cursor: pointer; }
    #result { margin-top: 1.5rem; padding: 1rem; background: #f4f4f4; border-radius: 6px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>Profile Number Generator</h1>
  <p>Generates a random 9-digit number that passes the Luhn check.</p>
  <button id="generate">Generate Profile Number</button>
  <div id="result"></div>
  <script>
    document.getElementById('generate').addEventListener('click', async () => {
      const button = document.getElementById('generate');
      const result = document.getElementById('result');
      button.disabled = true;
      result.textContent = 'Generating...';
      try {
        const res = await fetch('/api/generate');
        const data = await res.json();
        result.textContent = JSON.stringify(data, null, 2);
      } catch (err) {
        result.textContent = 'Error generating profile number.';
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(INDEX_HTML)


@app.get("/api/generate")
def generate():
    profile_number = profile_number_generator.generate_unique_random_profile_number()
    valid = is_valid_number(profile_number, calculate_luhn_check_digit)
    return jsonify({"profile_number": profile_number, "valid": valid})


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
