# Deployment Guide

The dashboard is a Flask app that reuses the dissertation's saved artifacts. No
retraining happens at runtime. Total resident memory is approximately 250 MB
(89 MB RF joblib + 117 MB RF SHAP explainer + ~40 MB everything else), so
**gunicorn is configured for 1 worker**. Two workers would not fit on the free
tiers of Render, Railway, or Fly.io.

Set `APP_USERNAME` and `APP_PASSWORD` to enable HTTP Basic auth. Leave them
unset for local development. The auth gate is not institutional SSO — replace
with OAuth/SAML before production rollout.

---

## Render (free tier fits — recommended first)

Render's free web service has 512 MB RAM, which is enough for one worker.

### One-time setup

1. Push this repo to GitHub. From the project root:
   ```bash
   git init && git add . && git commit -m "OULAD student-failure XAI dashboard"
   git branch -M main
   git remote add origin git@github.com:<your-github-username>/oulad-dashboard.git
   git push -u origin main
   ```
2. Sign in at <https://render.com> with your GitHub account.
3. Click **New → Blueprint**, point it at the new repo. Render will read
   [`render.yaml`](render.yaml) and create a `free` Docker web service
   preconfigured with `healthCheckPath: /healthz`.
4. Before the first deploy, set the two secrets Render asks for under
   **Environment**:
   - `APP_USERNAME` — e.g. `tutor`
   - `APP_PASSWORD` — a strong password (Render hides the value once saved)
5. Click **Apply** / **Deploy**. The first deploy builds the Docker image
   (≈ 60–90 s) and then runs the web service. Cold start of the live
   application (loading models + running self-tests) is ~25 s on free tier.

### After deploy

- Your dashboard is at `https://oulad-dashboard.onrender.com/`.
- HTTP Basic auth is on — visitors will see a browser password prompt before
  any page renders. `/healthz` stays public so Render can probe it.
- The free tier spins down after **15 min of idle**. Render's
  `healthCheckPath` keeps it warm only while the platform's own monitor is
  active. For snappy UX even after idle, set up **UptimeRobot** (free
  tier) to GET `https://oulad-dashboard.onrender.com/healthz` every 14 min.

### Limits of the free tier

- 512 MB RAM — we run 1 worker to stay under this.
- Spins down after 15 min idle without UptimeRobot.
- Free tier sleeps after 750 hours/month of usage (≈ all of a typical month
  for a single user); reset on the 1st of the month.
- For supervisor review or any non-trivial traffic, upgrade to the $7/mo
  Starter plan: same image, no sleep, 512 MB RAM.

### Updating the live site

Push to `main` on GitHub; Render's auto-deploy rebuilds and restarts. Plan
for ~90 s of downtime during redeploy. The first request after restart
cold-starts the model loader (~25 s).

---

## Railway (5 USD/mo after free trial)

Railway is the simplest platform if Render's free-tier spin-down is
unacceptable.

1. Connect this repository as a new project at <https://railway.app>.
2. Railway auto-detects the `Procfile`; if not, set the start command to
   `gunicorn app:app --workers 1 --timeout 120 --bind 0.0.0.0:$PORT`.
3. Add environment variables:
   - `APP_USERNAME` = (e.g.) `tutor`
   - `APP_PASSWORD` = (a strong secret)
4. Deploy. Cold start is similar to Render. **Railway does not spin down
   idle services on the paid plan**, so no keep-alive cron is needed.

---

## Fly.io (smallest cold start; pay-as-you-go)

Fly.io has the fastest cold start but its smallest machine is 256 MB —
**not enough** for this app (RF SHAP explainer alone is 117 MB). Use the
`shared-cpu-1x` 512 MB machine, or `performance-1x` 2 GB for headroom.

1. Install the Fly CLI and run `fly launch` in the project root. It detects
   the Dockerfile and creates a `fly.toml`.
2. Set secrets:
   ```bash
   fly secrets set APP_USERNAME=tutor APP_PASSWORD='<strong secret>'
   ```
3. Scale to a single machine (memory-bound):
   ```bash
   fly scale count 1
   fly scale memory 512
   ```
4. Deploy: `fly deploy`.

---

## Local development

```bash
# inside the project venv
pip install -r requirements.txt

# Linux / macOS:
flask run        # dev server, debug mode
# or:
gunicorn app:app --workers 1 --timeout 120 --bind 127.0.0.1:5000

# Windows: gunicorn does not run on Windows (missing fcntl). Use either:
flask run
# or, for a production-like WSGI server on Windows:
waitress-serve --port=5000 app:app

# open http://127.0.0.1:5000
```

Auth is disabled when `APP_USERNAME` / `APP_PASSWORD` are not set.

---

## Verification checklist (any platform)

1. `flask run` succeeds; no import errors.
2. `/`, `/global`, `/local-cases`, `/about`, `/predict` all render.
3. `/student/0` renders with predictions and waterfall JSON.
4. POST `/predict` returns 200 with both LR and RF SHAP inline (~0.6 s).
5. Picker typeahead on `/predict` returns ≥1 match within 1 s of typing.
6. Confusion-matrix cells on `/` match `outputs/tables/confusion_lr.csv`.
7. With auth env vars set, all pages return 401 until valid credentials are
   supplied. `/healthz` stays public.
8. `docker build -t oulad-dash . && docker run -p 5000:5000 oulad-dash`
   serves the same content.
9. Cold start is under 30 s from container start to first 200 OK.
