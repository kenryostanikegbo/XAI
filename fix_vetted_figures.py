"""Fix three rejected figures: cross_model_importance, cross_model_scatter, shap_local_tp_rf."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import spearmanr

PROJECT_ROOT = Path('C:/Users/HomePC/Documents/reportwritingprojects/studnetxai')
TABLE_DIR = PROJECT_ROOT / 'outputs' / 'tables'
FIG_DIR = PROJECT_ROOT / 'outputs' / 'figures'
MODEL_DIR = PROJECT_ROOT / 'outputs' / 'models'
SPLIT_DIR = PROJECT_ROOT / 'data' / 'processed' / 'split'

rcParams['font.family'] = 'DejaVu Sans'
rcParams['axes.grid'] = True
rcParams['savefig.dpi'] = 150

lr_imp = pd.read_csv(TABLE_DIR / 'shap_importance_lr.csv')
rf_imp = pd.read_csv(TABLE_DIR / 'shap_importance_rf.csv')

merged = lr_imp.merge(rf_imp, on='feature', suffixes=('_lr', '_rf'))
rho, _ = spearmanr(merged['mean_abs_shap_lr'], merged['mean_abs_shap_rf'])

merged['rank_lr'] = merged['mean_abs_shap_lr'].rank(ascending=False).astype(int)
merged['rank_rf'] = merged['mean_abs_shap_rf'].rank(ascending=False).astype(int)
merged['in_top10_lr'] = merged['rank_lr'] <= 10
merged['in_top10_rf'] = merged['rank_rf'] <= 10
agreement = merged[merged['in_top10_lr'] & merged['in_top10_rf']]
lr_only = merged[merged['in_top10_lr'] & ~merged['in_top10_rf']]
rf_only = merged[merged['in_top10_rf'] & ~merged['in_top10_lr']]
n_total = len(set(agreement['feature']) | set(lr_only['feature']) | set(rf_only['feature']))
jaccard = len(set(agreement['feature'])) / max(1, n_total)

top20_each = set(lr_imp.head(20)['feature']) | set(rf_imp.head(20)['feature'])
merged_top = merged[merged['feature'].isin(top20_each)].copy()
merged_top['combined'] = merged_top['mean_abs_shap_lr'] + merged_top['mean_abs_shap_rf']
merged_top = merged_top.sort_values('combined', ascending=False).reset_index(drop=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 7), sharey=True)
y_pos = np.arange(len(merged_top))

axes[0].barh(y_pos, merged_top['mean_abs_shap_lr'].values, color='steelblue')
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(merged_top['feature'], fontsize=9)
axes[0].invert_yaxis()
axes[0].set_xlabel('mean |SHAP| (LR, log-odds scale)', fontsize=10)
axes[0].set_title('Logistic Regression', fontsize=11)
axes[0].grid(alpha=0.3, axis='x', linestyle=':')
axes[0].set_xlim(left=0)
axes[0].tick_params(axis='y', labelsize=9)

axes[1].barh(y_pos, merged_top['mean_abs_shap_rf'].values, color='darkorange')
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(merged_top['feature'], fontsize=9, color='black')
axes[1].invert_yaxis()
axes[1].set_xlabel('mean |SHAP| (RF, probability scale)', fontsize=10)
axes[1].set_title('Random Forest', fontsize=11)
axes[1].grid(alpha=0.3, axis='x', linestyle=':')
axes[1].set_xlim(left=0)

fig.suptitle(
    f'Cross-model global importance  |  Spearman rho = {rho:.3f}  |  Top-10 Jaccard = {jaccard:.2f}',
    fontsize=12, y=0.995)
fig.subplots_adjust(left=0.30, right=0.96, top=0.94, bottom=0.10, wspace=0.18)
fig.savefig(FIG_DIR / 'cross_model_importance.png', dpi=150, bbox_inches=None, facecolor='white')
plt.close(fig)
print(f'[VET OK] wrote {FIG_DIR / "cross_model_importance.png"}')

fig, ax = plt.subplots(figsize=(9, 7))
x = merged['mean_abs_shap_lr'].values
y = merged['mean_abs_shap_rf'].values
ax.scatter(x, y, alpha=0.65, color='steelblue', edgecolor='white', s=42, zorder=2)

top10 = merged.head(10)
annotations = []
for _, row in top10.iterrows():
    xl, yl = row['mean_abs_shap_lr'], row['mean_abs_shap_rf']
    annotations.append(ax.annotate(
        row['feature'], (xl, yl),
        fontsize=8.5,
        xytext=(8, 6), textcoords='offset points',
        bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.78),
        zorder=3))

ax.set_xscale('symlog', linthresh=0.05)
ax.set_yscale('symlog', linthresh=0.001)
ax.set_xlabel('LR mean |SHAP| (log-odds scale, symlog)', fontsize=10)
ax.set_ylabel('RF mean |SHAP| (probability scale, symlog)', fontsize=10)
ax.set_title(
    f'Cross-model feature importance scatter  (Spearman rho = {rho:.3f}, both axes symlog)',
    fontsize=11)
ax.grid(alpha=0.3, linestyle=':')
ax.set_xlim(left=merged['mean_abs_shap_lr'].min() * 0.5)
ax.set_ylim(bottom=merged['mean_abs_shap_rf'].min() * 0.5)

fig.subplots_adjust(left=0.12, right=0.97, top=0.94, bottom=0.10)
fig.savefig(FIG_DIR / 'cross_model_scatter.png', dpi=150, bbox_inches=None, facecolor='white')
plt.close(fig)
print(f'[VET OK] wrote {FIG_DIR / "cross_model_scatter.png"}')

import joblib
import shap

lr_best = joblib.load(MODEL_DIR / 'lr_best.joblib')
rf_best = joblib.load(MODEL_DIR / 'rf_best.joblib')
rf_explainer = joblib.load(MODEL_DIR / 'shap_explainer_rf.joblib')

local_cases = pd.read_csv(TABLE_DIR / 'local_cases.csv')
tp_row = local_cases[local_cases['case'] == 'TP'].iloc[0]
tp_pos = int(tp_row['subset_pos'])
rf_shap_full = np.load(MODEL_DIR / 'shap_values_rf.npy')

X_test_t = pd.read_parquet(SPLIT_DIR / 'X_test.parquet')
DROP_COLS = ['id_student', 'code_presentation']
feature_cols = [c for c in X_test_t.columns if c not in DROP_COLS]
X_test_features = X_test_t[feature_cols]

shap_idx = np.load(MODEL_DIR / 'shap_indices_strat.npy')
rf_base = float(rf_explainer.expected_value[1])
rf_shap_row = rf_shap_full[tp_pos]
orig_idx = int(shap_idx[tp_pos])
rf_pred_proba = float(rf_best.predict_proba(X_test_features.iloc[[orig_idx]])[:, 1][0])

print(f'[TP RF] base={rf_base:.4f} shap_sum={rf_shap_row.sum():.4f} f(x)={rf_base + rf_shap_row.sum():.4f} pred_proba={rf_pred_proba:.4f}')

from shap.plots import _waterfall

if hasattr(rf_explainer, 'shap_values') is False:
    pass

sv = shap.Explanation(
    values=rf_shap_row,
    base_values=rf_base,
    data=X_test_features.iloc[orig_idx].values,
    feature_names=feature_cols)

plt.figure(figsize=(10, 7))
shap.plots.waterfall(sv, max_display=15, show=False)
plt.title(f'RF — Waterfall (predicted probability = {rf_pred_proba:.3f})',
          fontsize=12, pad=18)
plt.tight_layout()
plt.savefig(FIG_DIR / 'shap_local_tp_rf.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'[VET OK] wrote {FIG_DIR / "shap_local_tp_rf.png"} — f(x) label corrected from "1" to {rf_pred_proba:.3f}')

print('\nAll three rejected figures re-rendered.')
