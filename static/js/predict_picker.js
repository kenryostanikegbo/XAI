// Typeahead picker for the live-prediction form.
// Searches /student/search.json over the 300-row stratified SHAP subset.
// On selection: fetches /student/<row_idx>/features.json and populates the form.

(function () {
  "use strict";

  var input = document.getElementById("picker-input");
  var list = document.getElementById("picker-list");
  var status = document.getElementById("picker-status");
  var form = document.getElementById("predict-form");
  if (!input || !list || !form) return;

  var debounceId = null;
  var activeIndex = -1;
  var lastResults = [];

  function setStatus(text) {
    if (status) status.textContent = text || "";
  }

  function setExpanded(open) {
    input.setAttribute("aria-expanded", open ? "true" : "false");
    list.hidden = !open;
  }

  function riskClass(lr, rf) {
    // Average of both classifier probabilities; colour bucket matches the
    // dissertation's confusion matrix narrative.
    var avg = (lr + rf) / 2;
    if (avg >= 0.7) return "risk-high";
    if (avg >= 0.4) return "risk-med";
    return "risk-low";
  }

  function render(results) {
    lastResults = results;
    activeIndex = -1;
    list.innerHTML = "";
    if (!results.length) {
      setExpanded(false);
      setStatus("No matches.");
      return;
    }
    setExpanded(true);
    setStatus(results.length + " match" + (results.length === 1 ? "" : "es") + " in the 300-row SHAP subset.");

    for (var i = 0; i < results.length; i++) {
      var r = results[i];
      var li = document.createElement("li");
      li.setAttribute("role", "option");
      li.setAttribute("data-row-idx", String(r.row_idx));
      li.className = riskClass(r.lr_proba, r.rf_proba);

      var idEl = document.createElement("span");
      idEl.className = "picker-id";
      idEl.textContent = r.id_student;

      var metaEl = document.createElement("span");
      metaEl.className = "picker-meta";
      metaEl.textContent =
        r.code_module + " · " + r.code_presentation + " · row " + r.row_idx;

      var probEl = document.createElement("span");
      probEl.className = "picker-prob";
      probEl.innerHTML =
        "LR " + (r.lr_proba * 100).toFixed(1) + "%" +
        " · RF " + (r.rf_proba * 100).toFixed(1) + "%" +
        " · true " + (r.y_true === 1 ? "Fail" : "Pass");

      li.appendChild(idEl);
      li.appendChild(metaEl);
      li.appendChild(probEl);
      list.appendChild(li);
    }
  }

  function fetchResults(q) {
    var url = "/student/search.json?q=" + encodeURIComponent(q) + "&limit=20";
    fetch(url, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        render(data.results || []);
      })
      .catch(function (e) {
        list.innerHTML = "";
        setExpanded(false);
        setStatus("Search failed: " + e.message);
      });
  }

  function highlight(idx) {
    var items = list.children;
    for (var i = 0; i < items.length; i++) {
      items[i].classList.toggle("active", i === idx);
    }
    activeIndex = idx;
  }

  function selectIndex(idx) {
    if (idx < 0 || idx >= lastResults.length) return;
    var r = lastResults[idx];
    setStatus("Loading row " + r.row_idx + "…");
    setExpanded(false);
    fetch("/student/" + r.row_idx + "/features.json", { credentials: "same-origin" })
      .then(function (resp) {
        if (!resp.ok) throw new Error("HTTP " + resp.status);
        return resp.json();
      })
      .then(function (feats) {
        for (var k in feats) {
          if (!feats.hasOwnProperty(k)) continue;
          var el = form.elements[k];
          if (!el) continue;
          var v = feats[k];
          el.value = typeof v === "number" ? String(v) : v;
        }
        input.value = r.id_student;
        setStatus(
          "Loaded id_student " + r.id_student +
          " (row " + r.row_idx + "). Press Predict to score."
        );
        form.scrollIntoView({ behavior: "smooth", block: "start" });
      })
      .catch(function (e) {
        setStatus("Could not load row: " + e.message);
      });
  }

  input.addEventListener("input", function () {
    if (debounceId) clearTimeout(debounceId);
    var q = input.value.trim();
    debounceId = setTimeout(function () {
      fetchResults(q);
    }, 120);
  });

  input.addEventListener("focus", function () {
    if (input.value.trim() === "" && lastResults.length === 0) {
      fetchResults("");
    } else if (lastResults.length) {
      setExpanded(true);
    }
  });

  input.addEventListener("blur", function () {
    // Defer so a click on a list item still registers.
    setTimeout(function () { setExpanded(false); }, 150);
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (!lastResults.length) return;
      highlight(Math.min(activeIndex + 1, lastResults.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (!lastResults.length) return;
      highlight(Math.max(activeIndex - 1, 0));
    } else if (e.key === "Enter") {
      if (activeIndex >= 0) {
        e.preventDefault();
        selectIndex(activeIndex);
      }
    } else if (e.key === "Escape") {
      setExpanded(false);
    }
  });

  list.addEventListener("mousedown", function (e) {
    var li = e.target.closest("li[data-row-idx]");
    if (!li) return;
    e.preventDefault();
    var idx = parseInt(li.getAttribute("data-row-idx"), 10);
    var match = lastResults.findIndex(function (r) { return r.row_idx === idx; });
    if (match >= 0) selectIndex(match);
  });

  // Prime the picker with the first 20 rows so the dropdown shows something
  // before the user types.
  fetchResults("");
})();
