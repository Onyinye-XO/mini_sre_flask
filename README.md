This is a simple Flask app that simulates Site Reliability Engineering concepts like slow responses and random failures, with a built-in monitoring dashboard.

## Routes
- `/` — Health check
- `/slow` — Simulates a 5 second delay
- `/fail` — Randomly returns success or error
- `/dashboard` — Live metrics dashboard

## Setup
1. Clone the repo
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `.venv\Scripts\Activate.ps1`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python mini_sre.py`