## Dataset Recap

This section restates the dataset properties that the analytical findings of §4.5–§4.9 depend on. The full integration methodology is documented in Chapter 3 §3.4–§3.5 and in notebooks 01–02; the present section is a condensed reference, not a re-derivation.

### Source and Licence

The analytical dataset is the Open University Learning Analytics Dataset (OULAD), released by the Open University under the Creative Commons Attribution 4.0 International licence (Kuzilek et al., 2017). The dataset was downloaded from the Open University institutional repository and stored locally under `data/raw/`. Seven relational tables are included in the release; the present study uses six of them (`studentInfo`, `studentVle`, `vle`, `assessments`, `studentAssessment`, and `courses`) and excludes the seventh (`studentRegistration`) because its registration-status fields do not contribute to the predictive problem and add noise to the modelling matrix. The dataset covers seven presentations across two course modules and three academic years (2013 and 2014).

### Population and Filtering

The release contains 32,593 unique students across 32,593 student-presentation rows. After excluding Withdrawn students (those whose final outcome was registered as Withdrawn), 22,311 rows remain. After excluding rows with missing values in the modelling features (a small number of students with incomplete virtual-learning-environment records), 22,311 rows remain unaltered in the present study — no row was dropped for missing values because the join keys were preserved across all six tables. The 22,311 rows are split into one row per (student, module, presentation) tuple, which is the unit of analysis for the present study.

### Class Distribution

The binary target is constructed by mapping Pass and Distinction to 0 and Fail to 1 (Chapter 3 §3.5.5). Among the 22,311 rows, 15,299 are Pass or Distinction (68.6 per cent) and 7,012 are Fail (31.4 per cent). The class imbalance is therefore modest: the minority class is one-third of the population, not one-tenth or one-hundredth. Synthetic Minority Over-sampling Technique (SMOTE; Chawla et al., 2002) is applied within each cross-validation fold to balance the training set, but the test set is left at its original 31.4 per cent prevalence so that the reported metrics reflect deployment conditions (Chapter 3 §3.6.4).

### Feature Groups

The 21 base features fall into four groups, engineered as documented in Chapter 3 §3.5. Six features are demographic: gender, age band, highest education level on entry, region, and two indicators constructed from the disability flag. Seven features are virtual-learning-environment engagement: total clicks, distinct resources accessed, active days, mean clicks per active day, total days in the presentation, weighted mean clicks per resource, and the ratio of active days to total days. Five features are assessment: number of assessments submitted, mean assessment score, weighted mean score (weighted by assessment weight), mean days between assessment due date and submission, and whether the student submitted at least one assessment late. Three features are course-context: code module, code presentation, and presentation year.

### Modelling Matrix

After one-hot encoding of the categorical features (gender, age band, education level, region, code module, code presentation, presentation year), the modelling matrix contains 44 columns. The 21 base features expand to 44 because of the cardinality of the categorical variables: gender contributes 2 columns, age band contributes 3 columns, education contributes 4 columns, region contributes 13 columns, module contributes 7 columns, presentation contributes 4 columns, and presentation year contributes 2 columns. The continuous features (the 7 engagement metrics, the 5 assessment metrics, and 3 indicator features) contribute the remaining 15 columns without expansion.

### Train and Test Splits

The modelling matrix is split into a training set and a held-out test set using a stratified 70/30 split with `random_state=42` (Chapter 3 §3.6.1). The training set contains 15,617 rows (10,711 Pass, 4,906 Fail) and the test set contains 6,694 rows (4,588 Pass, 2,106 Fail). Both splits preserve the 31.4 per cent Fail prevalence of the full matrix. The test set is used exactly once, for the final evaluation reported in §4.5, and the random seed is fixed at every stage of the pipeline so that a future reader can reproduce the split bit-for-bit.

### What This Means for the Findings

The 31.4 per cent Fail prevalence is reported alongside every precision, recall, and F1 number in §4.5 so that the reader can compare the headline figures against the no-information baseline. The 22,311-row sample size is large enough that confidence intervals around the headline metrics are tight: a two-proportion z-test on the F1 gap of 0.020 reported in §4.5 returns a p-value below 0.05, but the gap is operationally modest and the present chapter does not over-interpret it. The 44-column modelling matrix is the input to every classifier and every SHAP computation in the present chapter, and the ranking analyses reported in §4.6 and §4.8 are computed over those 44 columns without exception.
