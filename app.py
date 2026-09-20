"""Flask app factory for the OULAD student-failure XAI dashboard.

Run locally with:
    flask run

Run in production with:
    gunicorn app:app --workers 1 --timeout 120

The dashboard reuses the dissertation's trained artifacts in outputs/models/
and outputs/figures/. No retraining happens at runtime.

Auth: set APP_USERNAME and APP_PASSWORD env vars to enable HTTP Basic auth.
Leave them unset for local development.
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from services import auth, cases, encoder, loader, predictor, search

PROJECT_ROOT = Path(__file__).resolve().parent
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"


def _figure_url(filename: str) -> str:
    """Build the URL for a figure in outputs/figures/."""
    return url_for("serve_figure", filename=filename)


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Required for flash() (used to surface form errors). Random per process
    # restart — flash messages are not security-sensitive, they just survive a
    # redirect within one request. If we ever use signed sessions for auth,
    # this becomes part of the threat model.
    app.config["SECRET_KEY"] = os.environ.get(
        "FLASK_SECRET_KEY", os.urandom(32).hex()
    )

    # Warm models and run predictor self-test at first request, NOT at import
    # time. Gunicorn forks workers; doing work in module scope would duplicate
    # the load. First request from each worker pays the cold-start cost.
    @app.before_request
    def _ensure_warm():
        if not loader.is_warmed():
            loader.warm()
            predictor.run_self_tests()

    # ---- Static figure route ----
    @app.route("/figures/<path:filename>")
    def serve_figure(filename: str):
        # send_from_directory is safe against path traversal.
        return send_from_directory(FIGURES_DIR, filename)

    # ---- Pages ----
    @app.route("/")
    @auth.requires_auth
    def index():
        import pandas as pd

        metrics = pd.read_csv(
            PROJECT_ROOT / "outputs" / "tables" / "metrics_comparison.csv"
        ).to_dict(orient="records")
        winners = pd.read_csv(
            PROJECT_ROOT / "outputs" / "tables" / "metric_winners.csv"
        ).to_dict(orient="records")
        conf_lr = pd.read_csv(
            PROJECT_ROOT / "outputs" / "tables" / "confusion_lr.csv", index_col=0
        )
        conf_rf = pd.read_csv(
            PROJECT_ROOT / "outputs" / "tables" / "confusion_rf.csv", index_col=0
        )
        return render_template(
            "index.html",
            metrics=metrics,
            winners=winners,
            conf_lr=conf_lr.values.tolist(),
            conf_rf=conf_rf.values.tolist(),
            roc_url=_figure_url("roc_curves.png"),
            pr_url=_figure_url("pr_curves.png"),
        )

    @app.route("/global")
    @auth.requires_auth
    def global_page():
        import pandas as pd

        shap_lr = pd.read_csv(
            PROJECT_ROOT / "outputs" / "tables" / "shap_importance_lr.csv"
        )
        shap_rf = pd.read_csv(
            PROJECT_ROOT / "outputs" / "tables" / "shap_importance_rf.csv"
        )
        cross_summary = pd.read_csv(
            PROJECT_ROOT / "outputs" / "tables" / "cross_model_summary.csv"
        ).to_dict(orient="records")
        # Cross-model comparison table (LR-only, RF-only, shared)
        cross_comp = pd.read_csv(
            PROJECT_ROOT / "outputs" / "tables" / "cross_model_comparison.csv"
        ).to_dict(orient="records")
        return render_template(
            "global.html",
            shap_lr_top10=shap_lr.head(10).to_dict(orient="records"),
            shap_rf_top10=shap_rf.head(10).to_dict(orient="records"),
            cross_summary=cross_summary,
            cross_comp=cross_comp,
            summary_lr_url=_figure_url("shap_summary_lr.png"),
            summary_rf_url=_figure_url("shap_summary_rf.png"),
            importance_lr_url=_figure_url("shap_importance_lr.png"),
            importance_rf_url=_figure_url("shap_importance_rf.png"),
            cross_importance_url=_figure_url("cross_model_importance.png"),
            cross_scatter_url=_figure_url("cross_model_scatter.png"),
        )

    @app.route("/local-cases")
    @auth.requires_auth
    def local_cases_page():
        return render_template("local_cases.html", cases=cases.list_cases())

    @app.route("/student/<int:row_idx>")
    @auth.requires_auth
    def student_page(row_idx: int):
        try:
            pred = predictor.predict_one(row_idx)
        except IndexError:
            abort(404)
        has_rf_shap = predictor.shap_subset_position_for(row_idx) is not None
        X = loader.X_test()
        row = X.iloc[row_idx]

        # If this row_idx is one of the 6 canonical cases, serve the pre-rendered
        # waterfall PNGs directly. Otherwise the JSON view is the only option.
        canonical_lr_png = None
        canonical_rf_png = None
        try:
            case = cases.get_case_by_row_idx(row_idx)
            slug = case.case.lower()
            canonical_lr_png = _figure_url(f"shap_local_{slug}_lr.png")
            canonical_rf_png = _figure_url(f"shap_local_{slug}_rf.png")
        except KeyError:
            pass

        return render_template(
            "student.html",
            row_idx=row_idx,
            id_student=int(row["id_student"]),
            code_presentation=str(row["code_presentation"]),
            pred=pred,
            has_rf_shap=has_rf_shap,
            canonical_lr_png=canonical_lr_png,
            canonical_rf_png=canonical_rf_png,
        )

    @app.route("/student/<int:row_idx>/shap.json")
    @auth.requires_auth
    def student_shap_json(row_idx: int):
        try:
            explanation = predictor.explain_one(row_idx)
        except IndexError:
            abort(404)
        from services.feature_schema import feature_columns
        return jsonify(
            {
                "row_idx": row_idx,
                "features": list(feature_columns()),
                "lr_shap": explanation.lr_shap,
                "rf_shap": explanation.rf_shap,
            }
        )

    @app.route("/student/<int:row_idx>/features.json")
    @auth.requires_auth
    def student_features_json(row_idx: int):
        """Return the 21-feature dict for a test-set row, for form prefill."""
        try:
            feats = encoder.default_features_from_row(row_idx)
        except (IndexError, KeyError):
            abort(404)
        return jsonify(feats)

    @app.route("/student/search.json")
    @auth.requires_auth
    def student_search_json():
        """Search the full X_test set by id_student substring.

        Query params: q (substring), limit (default 20, capped at 100).
        Returns a JSON list of compact row summaries for the picker.
        """
        q = request.args.get("q", "").strip()
        try:
            limit = int(request.args.get("limit", "20"))
        except ValueError:
            limit = 20
        limit = max(1, min(100, limit))
        return jsonify({"results": search.search(q, limit=limit)})

    # ---- Live prediction form ----

    def _default_features() -> dict:
        """First test-set row as a sensible prefill so the user sees a real
        student without having to type anything. Row 0 is a Pass by both
        classifiers (low risk profile), which makes the form a useful demo."""
        return encoder.default_features_from_row(0)

    @app.route("/predict", methods=["GET"])
    @auth.requires_auth
    def predict_form():
        feats = _default_features()
        n_avail = encoder.N_ASSESSMENTS_AVAILABLE.get(
            (feats["code_module"], feats["code_presentation"]), "?"
        )
        return render_template(
            "predict.html",
            features=feats,
            opts=encoder.form_options(),
            max_assessments_available=n_avail,
        )

    @app.route("/predict", methods=["POST"])
    @auth.requires_auth
    def predict_submit():
        # Form fields are raw strings; coerce them here.
        raw = request.form.to_dict()
        try:
            features = {
                "gender": raw["gender"],
                "age_band": raw["age_band"],
                "region": raw["region"],
                "highest_education": raw["highest_education"],
                "imd_band": raw.get("imd_band") or "?",
                "num_of_prev_attempts": int(raw["num_of_prev_attempts"]),
                "total_clicks": float(raw["total_clicks"]),
                "active_days": float(raw["active_days"]),
                "max_daily_clicks": float(raw["max_daily_clicks"]),
                "distinct_resources": float(raw["distinct_resources"]),
                "early_clicks_14d": float(raw["early_clicks_14d"]),
                "weekend_click_ratio": float(raw["weekend_click_ratio"]),
                "assessments_submitted": float(raw["assessments_submitted"]),
                "mean_assessment_score": float(raw["mean_assessment_score"]),
                "weighted_mean_score": float(raw["weighted_mean_score"]),
                "mean_days_to_submit": float(raw["mean_days_to_submit"]),
                "code_module": raw["code_module"],
                "code_presentation": raw["code_presentation"],
            }
        except (KeyError, ValueError) as e:
            flash(f"Invalid input: {e}", "error")
            merged = {**_default_features(), **{k: v for k, v in raw.items() if isinstance(v, str)}}
            n_avail = encoder.N_ASSESSMENTS_AVAILABLE.get(
                (merged["code_module"], merged["code_presentation"]), "?"
            )
            return render_template(
                "predict.html",
                features=merged,
                opts=encoder.form_options(),
                max_assessments_available=n_avail,
            ), 400

        try:
            result = predictor.predict_and_explain_from_features(features)
        except encoder.EncodingError as e:
            flash(str(e), "error")
            n_avail = encoder.N_ASSESSMENTS_AVAILABLE.get(
                (features["code_module"], features["code_presentation"]), "?"
            )
            return render_template(
                "predict.html",
                features=features,
                opts=encoder.form_options(),
                max_assessments_available=n_avail,
            ), 400

        return render_template(
            "result.html",
            features=features,
            result=result,
            model_disagreement=result.lr_pred != result.rf_pred,
        )

    @app.route("/about")
    @auth.requires_auth
    def about_page():
        return render_template("about.html")

    @app.route("/healthz")
    def healthz():
        # No auth on /healthz so keep-alive cron can ping without credentials.
        return ("ok", 200)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
