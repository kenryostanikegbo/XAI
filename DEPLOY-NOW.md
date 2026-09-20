# Make this dashboard live — checklist

The repo is ready to push. Three steps. ~10 minutes.

## 1. Push to GitHub (~2 min)

1. Create an empty repo at <https://github.com/new> — name it
   `oulad-dashboard`, **don't** initialise it with a README.
2. From this project root, run:
   ```bash
   git remote add origin git@github.com:<your-github-username>/oulad-dashboard.git
   git push -u origin main
   ```
   (Replace the SSH URL with the HTTPS one if you don't have SSH keys
   set up: `https://github.com/<you>/oulad-dashboard.git`)
3. Verify the push by visiting your GitHub repo — you should see 116
   files, ~50 MB total.

## 2. Deploy to Render (~5 min)

1. Sign in at <https://render.com> with your GitHub account.
2. Click **New → Blueprint**, point at `oulad-dashboard`.
3. Render reads `render.yaml` and shows a plan to create one `web`
   service named `oulad-dashboard` on the **free** plan with
   `healthCheckPath: /healthz`. Click **Apply**.
4. Render builds the Docker image (≈ 90 s) and starts the web service.
   The first request cold-starts the model loader (~25 s).
5. Your dashboard is live at `https://oulad-dashboard.onrender.com/`.

## 3. Enable auth (~1 min)

1. In the Render dashboard, go to your service → **Environment**.
2. Add two variables (the YAML blueprint marked them `sync: false` so
   Render prompts you for them):
   - `APP_USERNAME` = `tutor`
   - `APP_PASSWORD` = a strong password (Render hides it after save)
3. Render redeploys automatically (~90 s).
4. Visit `https://oulad-dashboard.onrender.com/` — you should see a
   browser password prompt before any page renders.
5. The `/healthz` endpoint stays public so Render can probe it.

## 4. Optional: keep it warm

Free tier spins down after **15 minutes of idle**. For your supervisor's
demo to feel snappy:

1. Sign up at <https://uptimerobot.com> (free).
2. Add a new monitor: type **HTTP**, URL `https://oulad-dashboard.onrender.com/healthz`,
   interval **14 minutes**.
3. That's it. UptimeRobot pings the healthcheck, Render keeps the service
   warm.

## Verification after deploy

Open the dashboard in an incognito window so you're definitely
re-prompted for auth:

- `/` → model card with confusion matrices + ROC/PR figures
- `/global` → both beeswarms + bar plots
- `/feed` → 6 canonical cases (live link)
- `/predict` → form. Type into the picker, click an id_student row,
  press Predict → both classifiers' P(Fail) + both SHAP waterfalls in
  ~0.6 s.
- `/healthz` → plain 200 (no auth prompt)

## If anything goes wrong

- **Build fails on Render**: check the **Logs** tab. Most often a missing
  file. Run `git ls-files` locally and compare with `git ls-files` on
  Render (visible in the build log).
- **App 502s on first request**: the cold start exceeded the 60 s boot
  timeout. Wait, then retry — Render's healthcheck will eventually report
  healthy.
- **App OOM**: 512 MB RAM exceeded. We're at ~250 MB; if you added
  notebooks / raw data, exclude them from the image (`.dockerignore`).

## After the dissertation is signed off

The dashboard is a faithful deployment of the dissertation's trained
models — not a separate production system. Once your marker confirms
the work, you can either:

- Delete the Render service (free tier, no commitment), or
- Upgrade to a $7/mo Starter plan for permanent availability.

Either way, no re-training is needed; the dissertation's saved artifacts
in `outputs/models/` and `outputs/figures/` are exactly what the live
site serves.
