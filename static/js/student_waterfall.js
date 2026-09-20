// Inline SHAP waterfall renderer for ad-hoc student rows.
//
// Fetches /student/<row_idx>/shap.json and renders the top 10 features by |SHAP|
// into the #lr-waterfall and #rf-waterfall containers. Red bars push toward Fail
// (positive SHAP); blue bars push toward Pass (negative SHAP). Magnitudes are
// not comparable across the two models (LR in log-odds, RF in probability).
//
// Pure vanilla JS, no dependencies.

(function () {
  "use strict";

  function renderWaterfall(container, features, values, modelLabel) {
    if (!container) return;

    // Expose on window so the result page can call it after a deferred RF
    // SHAP fetch fills in the data-shap attribute.
    window.renderWaterfall = renderWaterfall;

    // Pair features with their SHAP values, sort by |SHAP| descending.
    var pairs = features.map(function (f, i) {
      return { feature: f, value: values[i] };
    });
    pairs.sort(function (a, b) {
      return Math.abs(b.value) - Math.abs(a.value);
    });
    var top10 = pairs.slice(0, 10);

    var maxAbs = top10.reduce(function (m, p) {
      return Math.max(m, Math.abs(p.value));
    }, 1e-9);

    container.innerHTML = "";

    if (values === null) {
      var note = document.createElement("div");
      note.className = "waterfall-empty";
      note.textContent =
        modelLabel +
        " SHAP not available for this row (outside the 300-row stratified subset).";
      container.appendChild(note);
      return;
    }

    top10.forEach(function (p) {
      var row = document.createElement("div");
      row.className = "waterfall-bar";

      var fLabel = document.createElement("span");
      fLabel.className = "feature";
      fLabel.textContent = p.feature;
      fLabel.title = p.feature;

      var track = document.createElement("span");
      track.className = "bar-track";
      var fill = document.createElement("span");
      fill.className = "bar-fill " + (p.value >= 0 ? "positive" : "negative");
      var pct = (Math.abs(p.value) / maxAbs) * 50.0; // half-track max
      fill.style.width = pct.toFixed(2) + "%";
      track.appendChild(fill);

      var vLabel = document.createElement("span");
      vLabel.className = "value";
      vLabel.textContent = (p.value >= 0 ? "+" : "") + p.value.toFixed(3);

      row.appendChild(fLabel);
      row.appendChild(track);
      row.appendChild(vLabel);
      container.appendChild(row);
    });
  }

  function loadAndRender(container) {
    var rowIdx = container.getAttribute("data-row-idx");
    var model = container.getAttribute("data-model");
    var label = model === "lr" ? "Logistic Regression" : "Random Forest";

    // Inline path: data-shap / data-features attributes set by the template
    // (used by /predict result when SHAP is computed live and not served via
    // a JSON endpoint). data-row-idx == "-1" is the sentinel for inline data.
    var inlineShap = container.getAttribute("data-shap");
    var inlineFeats = container.getAttribute("data-features");
    if (inlineShap && inlineFeats) {
      try {
        var values = JSON.parse(inlineShap);
        var features = JSON.parse(inlineFeats);
        renderWaterfall(container, features, values, label);
      } catch (e) {
        container.innerHTML =
          '<div class="waterfall-empty">Failed to render inline SHAP: ' +
          e.message +
          "</div>";
      }
      return;
    }

    fetch("/student/" + rowIdx + "/shap.json", { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        var values = model === "lr" ? data.lr_shap : data.rf_shap;
        renderWaterfall(container, data.features, values, label);
      })
      .catch(function (err) {
        container.innerHTML =
          '<div class="waterfall-empty">Failed to load SHAP: ' +
          err.message +
          "</div>";
      });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var lr = document.getElementById("lr-waterfall");
    var rf = document.getElementById("rf-waterfall");
    if (lr) loadAndRender(lr);
    if (rf) loadAndRender(rf);
  });
})();
