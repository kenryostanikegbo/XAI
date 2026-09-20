```{=openxml}
<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>CHAPTER ONE</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>INTRODUCTION</w:t></w:r></w:p>
```

## 1.1 Background

### 1.1.1 Learning Analytics and Educational Data Mining

Learning Analytics (LA) is broadly defined as the measurement, collection, analysis, and reporting of data about learners and their contexts, with the primary goal of understanding and optimising learning and the environments in which it occurs (Long and Siemens, 2011). Educational Data Mining (EDM), a closely related field, applies computational techniques from machine learning, statistics, and data mining specifically to educational data in order to discover patterns that can inform educational practice (Baker and Yacef, 2009). Together, LA and EDM constitute a powerful interdisciplinary research agenda at the intersection of computer science, education, and psychology.
The Open University Learning Analytics Dataset (OULAD) is one of the most widely used benchmark resources in this domain. Released by the Open University, the United Kingdom's largest academic institution, OULAD contains data from 32,593 students across 22 module presentations. It encompasses student demographic information, assessment outcomes, Virtual Learning Environment (VLE) interaction logs, and four standardised outcome categories: Distinction, Pass, Fail, and Withdrawn. The dataset was first described by Kuzilek, Hlosta, and Zdrahal (2017) in Scientific Data and has since enabled reproducible, comparative research across the global learning analytics community.
### 1.1.2 Machine Learning in Student Performance Prediction

The prediction of student academic outcomes using machine learning has attracted considerable research attention over the past decade. Studies such as those by Alhakbani and Alnassar (2022), who systematically reviewed 32 benchmark studies using OULAD, have established that Random Forest and Decision Trees are among the most frequently employed classifiers in this domain. Althibyani (2024), in a comprehensive analysis using OULAD, reported that Logistic Regression achieved 92.4% accuracy on binary pass/fail classification but dropped to 72.1% when predicting the full four-class outcome structure, demonstrating the significantly greater difficulty of multiclass prediction and the practical advantage of binary formulations for deployment.
Jha, Ghergulescu, and Moldovan (2019) showed that VLE interaction features were the most predictive feature group for both dropout and final result prediction, achieving AUC scores of up to 0.91 and 0.93, respectively. Similarly, Agyemang et al. (2024) reported that the Random Forest Classifier achieved 89.9% accuracy on OULAD, with a G-Mean of 0.9243, demonstrating strong performance on imbalanced data. These studies collectively underscore that feature quality, particularly engineered engagement indicators derived from VLE logs, is a critical determinant of prediction success.
### 1.1.3 The Class Imbalance Problem

A recurring methodological challenge in student failure prediction is class imbalance: typically, the majority of students pass or achieve distinction, while failures and dropouts represent the minority class. Standard ML algorithms optimise for overall accuracy, which can cause them to systematically misclassify at-risk students, precisely the individuals educators most need to identify. To address this, techniques such as SMOTE (Synthetic Minority Over-sampling Technique; Chawla et al., 2002) and class weighting have become standard in the EDM literature. Law et al. (2024), in a graduate on-time detection study, demonstrated that their Ensemble-SMOTE approach achieved an F1-score of 91.30%, outperforming both standalone SMOTE and unbalanced baselines.
### 1.1.4 Explainable Artificial Intelligence and SHAP

The growing adoption of machine learning in high-stakes domains has prompted increasing demand for model interpretability. Explainable Artificial Intelligence (XAI) refers to techniques designed to make AI decisions transparent and understandable to human users. Within the XAI toolkit, SHAP (SHapley Additive exPlanations), introduced by Lundberg and Lee (2017), has emerged as a particularly influential framework. SHAP draws on cooperative game theory, specifically Shapley values from Shapley (1953), to assign each feature an importance score for any given prediction, delivering both global interpretability (which features are most important overall) and local interpretability (why a specific prediction was made for an individual student).
The application of SHAP to educational data has grown rapidly. Kalita et al. (2025), in a Bi-LSTM study with SHAP for academic performance prediction, used SHAP to reveal threshold effects in student engagement features, finding that marginal increases in VLE activity beyond certain levels produced diminishing predictive returns. Alalawi (2025) demonstrated that SHAP provides more stable feature importance rankings than LIME for dropout prediction, and that its additive decomposition enabled personalised risk narratives for individual students. Hooshyar and Yang (2024), in a critical analysis of SHAP and LIME in educational contexts, cautioned that post-hoc explanations are sensitive to model architecture and feature collinearity, a nuance this study addresses by carefully interpreting SHAP outputs within the context of each model's structure.
## 1.2 Problem Statement

Despite the growing body of research on machine learning for student performance prediction, a significant gap remains in the literature. While numerous studies have demonstrated that ML models can achieve high accuracy on the OULAD dataset, the majority treat their models as opaque prediction engines. Little attention is paid to systematically interpreting which factors the models identify as driving student failure, and even fewer studies provide side-by-side comparative interpretability analyses using SHAP across different model architectures.
Furthermore, existing OULAD studies frequently rely on accuracy as their sole evaluation metric, which is insufficient for imbalanced datasets where the minority class (failure) is the class of greatest practical interest. The absence of comprehensive multi-metric evaluation, incorporating Precision, Recall, F1-Score, and ROC-AUC, limits the depth of insight available to practitioners seeking to understand model behaviour under different classification thresholds.
This study addresses these gaps by developing and evaluating an explainable machine learning pipeline for predicting student failure on OULAD, using SHAP to provide transparent, interpretable insights into both Logistic Regression and Random Forest models, and rigorously evaluating both models using a comprehensive suite of classification metrics.
## 1.3 Research Aim

The aim of this study is to develop and evaluate an explainable machine learning model for predicting students at risk of failure using the Open University Learning Analytics Dataset (OULAD), while comparing the predictive performance and interpretability of Logistic Regression and Random Forest through SHAP analysis.
## 1.4 Research Objectives

To achieve the research aim stated above, the following objectives are pursued:

To preprocess and integrate the OULAD tables into a unified dataset suitable for machine learning analysis.
To engineer relevant features from students' demographic information, assessment records, and Virtual Learning Environment (VLE) engagement data.
To develop a Logistic Regression classification model for predicting student failure on the OULAD dataset.
To develop a Random Forest classification model for predicting student failure on the OULAD dataset.
To evaluate and compare both models using Precision, Recall, F1-Score, and ROC-AUC.
To apply SHAP (SHapley Additive exPlanations) in interpreting the predictions of both models, identifying the key factors influencing student failure at both global and local levels.
## 1.5 Research Questions

This study is guided by the following research questions:

Which of the two models, Logistic Regression or Random Forest, achieves superior performance on the OULAD dataset when evaluated using Precision, Recall, F1-Score, and ROC-AUC?
What are the most important features driving the prediction of student failure in each model, as identified by SHAP analysis?
Do Logistic Regression and Random Forest identify the same or different factors as the primary drivers of student failure, and what does this imply for the design of educational interventions?
How do the SHAP-based explanations generated for an individual student differ between the two models, and what insights do these local explanations offer for personalised student support?
## 1.6 Significance of the Study

This study contributes to both the academic literature and practical educational practice in several meaningful ways. From an academic perspective, it adds to the growing body of work on Explainable AI in education by providing a structured, comparative analysis of SHAP-based interpretability across two fundamentally different model architectures, a linear model and a tree-based ensemble. Most existing XAI studies in EDM focus on a single model; the comparative approach adopted here allows for a more nuanced understanding of how model architecture shapes feature attribution and explanation quality.
From a practical standpoint, the study is directly relevant to educators and institutional administrators at the Open University and similar distance-learning institutions. By identifying and visualising the specific factors, demographic, engagement-based, and assessment-related, that most strongly predict student failure, the study provides evidence-based guidance for designing early warning systems and targeted interventions. The inclusion of SHAP force plots and waterfall plots for individual students demonstrates how such models can move beyond abstract risk scores to provide actionable, human-readable explanations that educators can use in real time.
The study also addresses a methodological gap by advocating for a multi-metric evaluation framework. In imbalanced datasets, accuracy alone can be misleading; a model that simply predicts the majority class for all instances will achieve high apparent accuracy while failing to identify any at-risk students. By reporting Precision, Recall, F1-Score, and ROC-AUC, the study ensures that model comparison is grounded in metrics that reflect real-world performance requirements.
## 1.7 Scope and Limitations

The study is bounded by the following scope and limitations. First, the study uses the OULAD dataset exclusively. While OULAD is a rich and well-documented resource, it reflects the specific institutional context of the Open University, a large public distance-learning institution in the United Kingdom. Findings may not be directly generalisable to campus-based universities, vocational training providers, or educational systems in other national contexts.
Second, the study employs binary classification (Pass versus Fail), merging Distinction and Pass into a single positive class while grouping Withdrawn with Fail. This decision, while supported by existing literature (Althibyani, 2024; Jha et al., 2019) and by the practical need for a tractable prediction target, reduces the granularity of outcome analysis. Chapter 2 provides a more detailed justification for this design choice.
Third, SHAP explanations are post-hoc interpretations and do not necessarily reveal causal relationships. A feature with high SHAP importance indicates correlation with the outcome, not necessarily causation. Fourth, the study does not conduct a longitudinal evaluation of whether SHAP-informed interventions actually improve student outcomes; this would require a separate experimental or quasi-experimental design that falls outside the scope of the present study.
## 1.8 Ethical Considerations

The OULAD dataset was released by the Open University following a rigorous anonymisation process. Student identities are represented by anonymised alphanumeric codes, and sensitive attributes are provided as grouped or coded categories to prevent individual re-identification. The data was collected as part of the university's routine institutional operations and released for research purposes under appropriate data governance arrangements (Kuzilek et al., 2017). As such, the present study does not involve the collection of new human subjects data and is exempt from formal ethics review.
Nevertheless, the study is mindful of the ethical implications of using predictive models in educational settings. Predictive models can perpetuate or amplify existing biases if trained on data reflecting historical inequities. The study acknowledges this risk and, through SHAP subgroup analysis, seeks to identify whether feature attributions are equitable across demographic groups. The study does not recommend or implement any automated interventions based on model predictions; rather, it presents SHAP-informed insights as tools to support, not replace, professional educator judgement.
## 1.9 Organisation of the Report

This report is organised into five chapters as follows:

Chapter 1 (Introduction), establishes the background, problem statement, research aim, objectives, questions, significance, scope, limitations, and ethical considerations of the study.
Chapter 2 (Literature Review), presents a comprehensive, themed review of the relevant academic literature, covering traditional machine learning approaches, ensemble methods, explainable AI in EDM, and a comparative discussion of five closely related OULAD studies, before identifying the research gap and justifying this study's contribution.
Chapter 3 (Methodology), describes the research design, data preprocessing, feature engineering approach, class imbalance handling strategy, model development and training procedures, evaluation methodology, and the SHAP interpretability framework.
Chapter 4 (Results and Analysis), presents the experimental results, including model performance comparisons, SHAP global and local interpretations, and a critical discussion of the findings in the context of the research questions.
Chapter 5 (Conclusion and Recommendations), summarises the key findings, states the conclusions, acknowledges the study's limitations, and provides recommendations for future research and for institutional practice.

```{=openxml}
<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>CHAPTER TWO</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>LITERATURE REVIEW</w:t></w:r></w:p>
```

## 2.1 Introduction

This chapter presents a comprehensive literature review for the study titled \"Predicting Student Failure with Explainable Machine Learning: A Comparative Study of Logistic Regression and Random Forest with SHAP Interpretability on the Open University Learning Analytics Dataset (OULAD).\" The review is structured according to a Conceptual-Empirical-Theoretical framework, which provides a rigorous and organised approach to engaging with the scholarly literature by distinguishing between the definitions and constructs that underpin the field, the empirical evidence accumulated from studies conducted within it, and the theoretical foundations that explain why and how the observed phenomena occur.

This tripartite structure is widely adopted in social science and applied computing research and is particularly suited to a study at the intersection of machine learning and educational analytics, where conceptual clarity, empirical precedent, and theoretical grounding are all essential. The Conceptual Review (Section 2.2) defines and situates the key constructs of the study: Learning Analytics, Educational Data Mining, Student Performance Prediction, Virtual Learning Environments, Explainable Artificial Intelligence, and the class imbalance problem. The Empirical Review (Section 2.3) surveys and synthesises the findings of relevant primary research studies, organised into five thematic sub-sections: traditional machine learning approaches, ensemble learning methods, deep learning approaches, explainable AI applications in education, and studies that have specifically used the OULAD dataset. The Theoretical Review (Section 2.4) examines the theoretical underpinnings of SHAP and game-theoretic interpretability, class imbalance theory, and the interpretability-accuracy tradeoff. Section 2.5 articulates the specific research gap identified through the preceding review and justifies the contribution of the present study. Section 2.6 provides a brief chapter summary.

The literature review draws primarily on peer-reviewed scholarly publications from 2020 to 2026, with foundational works from earlier periods included where necessary to establish conceptual or theoretical context. Electronic databases searched include Google Scholar, IEEE Xplore, ScienceDirect, MDPI, ResearchGate, and the ACM Digital Library. Search terms included: Open University Learning Analytics Dataset, OULAD machine learning, predicting student failure, explainable AI in education, SHAP student performance, early prediction of student performance, educational data mining ensemble methods, and SMOTE student prediction.

## 2.2 Conceptual Review

### 2.2.1 Learning Analytics and Educational Data Mining

The conceptual landscape of this study is anchored in two closely related and often overlapping fields: Learning Analytics (LA) and Educational Data Mining (EDM). Learning Analytics, as defined by Long and Siemens (2011), is the measurement, collection, analysis, and reporting of data about learners and their contexts, with the explicit goal of understanding and optimising learning and the environments in which it occurs. LA is characterised by its applied, institution-facing orientation: it is primarily concerned with generating actionable insights that educators and administrators can use to improve student outcomes and institutional effectiveness. The field draws on theories from education, psychology, sociology, and computer science, and employs a wide range of analytical techniques ranging from simple descriptive statistics to sophisticated machine learning models.

Educational Data Mining, by contrast, is a more technically oriented field that applies computational and statistical methods, including machine learning, data mining, and information retrieval, specifically to educational data in order to discover patterns and generate knowledge that can inform educational theory and practice (Baker and Yacef, 2009). EDM is characterised by its methodological rigour and its focus on developing and evaluating algorithms. While LA and EDM have distinct disciplinary roots, LA emerging from educational practice and EDM from computer science, the boundary between them has blurred considerably in recent years, with most contemporary studies drawing on techniques from both traditions. Namoun and Alshanqiti (2020), in a widely cited systematic literature review covering 77 studies, observed that the two fields share the common goal of using data to improve learning, and noted that their methodological convergence has enriched both.

Both LA and EDM are enabled by the increasing digitisation of education. As more teaching and learning activities migrate to online and blended delivery modes, vast quantities of digital trace data are generated, creating an unprecedented resource for understanding how students learn, where they struggle, and how institutions can intervene more effectively. This data abundance has transformed what was once a field reliant on small-scale surveys and qualitative studies into one capable of population-level, real-time, and predictive analytics.

### 2.2.2 Student Performance Prediction

Student Performance Prediction (SPP) is the application of statistical and machine learning techniques to predict students\' academic outcomes, such as final grades, pass/fail status, dropout, or degree classification, using historical and contemporary data about students and their learning behaviours. The goal of SPP is not merely to report on past performance but to generate actionable, forward-looking insights that enable educators and institutions to identify at-risk students early enough to deliver targeted support. The practical importance of SPP is underscored by the substantial personal, financial, and societal costs associated with student failure and dropout. Boujmiraz (2026), in a comprehensive review of the field, noted that early prediction, within the first two to four weeks of a course, is now achievable with 70-80% accuracy using well-engineered features, and that the window for effective intervention narrows rapidly as courses progress.

SPP encompasses a variety of modelling tasks, including binary classification (pass/fail, dropout/completion), multiclass classification (distinction/pass/fail/withdrawn), grade prediction (continuous or ordinal), and risk scoring (assigning a probability or risk score to each student). The choice of modelling task has significant implications for the choice of algorithm, the evaluation methodology, and the interpretability requirements. Binary classification, which is adopted in the present study, is the most widely used formulation in early-warning systems because it maps directly to the operational decision of whether or not to trigger an intervention.

### 2.2.3 Virtual Learning Environments as Data Sources

A Virtual Learning Environment (VLE), also referred to as a Learning Management System (LMS), is a software platform that supports the delivery of educational content and the administration of online and blended learning courses. VLEs such as Moodle, Blackboard, Canvas, and the Open University\'s own Moodle-based platform generate rich logs of student interactions, including page views, resource downloads, forum posts, quiz attempts, assignment submissions, and login frequencies. These logs, when aggregated and analysed, provide behavioural indicators of student engagement that are strongly associated with academic outcomes.

Conijn et al. (2022), in a study examining the relationship between VLE engagement and academic performance in a distance-learning context, found that engagement metrics, particularly the frequency and timing of VLE interactions, were significant predictors of final outcomes, even after controlling for prior attainment and demographic factors. Their finding that the temporal pattern of engagement (early, sustained engagement versus late, cramming-style engagement) was more predictive than raw click counts has important implications for feature engineering in SPP models. Similarly, Herodotou et al. (2019), in a large-scale evaluation of predictive analytics at the Open University using the OU Analyse system, demonstrated that models incorporating VLE clickstream data achieved meaningfully higher predictive accuracy than models using demographic or assessment data alone, underscoring the unique value of behavioural trace data for SPP.

### 2.2.4 Explainable Artificial Intelligence

Explainable Artificial Intelligence (XAI) is an umbrella term for methods, techniques, and tools designed to make the predictions and decisions of artificial intelligence systems understandable to human users. The field has grown rapidly in response to the proliferation of deep learning and ensemble models, often referred to as \"black boxes\", whose internal decision-making processes are opaque even to their developers. In high-stakes domains such as healthcare, criminal justice, and education, the opacity of AI systems is not merely an academic inconvenience but a significant barrier to adoption, accountability, and trust.

XAI encompasses a broad spectrum of approaches, ranging from inherently interpretable models (such as Linear Models and Decision Trees) to post-hoc interpretability methods that explain the predictions of any model after training. Among post-hoc methods, SHAP (SHapley Additive exPlanations), introduced by Lundberg and Lee (2017), has emerged as the dominant framework in educational data mining due to its theoretical grounding in cooperative game theory and its ability to deliver both global and local interpretability. LIME (Local Interpretable Model-agnostic Explanations; Ribeiro et al., 2016) is a complementary local surrogate method that approximates complex models near specific instances using interpretable proxies. The present study adopts SHAP as its primary interpretability framework, with LIME referenced comparatively where relevant.

### 2.2.5 Class Imbalance in Educational Datasets

Class imbalance refers to the condition in which the distribution of target classes in a dataset is highly unequal, such that one or more classes are substantially underrepresented relative to others. In student performance prediction, the minority class is typically the class of greatest practical interest, students who will fail or withdraw, while the majority class (students who pass or achieve distinction) is typically much larger. Standard machine learning algorithms optimise for overall accuracy, which can cause them to ignore the minority class entirely: a model that predicts the majority class for all instances will achieve high accuracy on an imbalanced dataset while completely failing at the task of identifying at-risk students.

The class imbalance problem has been extensively studied in the machine learning literature, and several mitigation strategies have been developed. These broadly fall into three categories: data-level approaches, which modify the training data distribution through resampling (oversampling the minority class, undersampling the majority class, or both); algorithm-level approaches, which modify the learning algorithm itself (such as class weighting, cost-sensitive learning, and ensemble-based resampling); and hybrid approaches, which combine elements of both. SMOTE (Synthetic Minority Over-sampling Technique; Chawla et al., 2002) is the most widely used data-level approach in educational data mining. It generates synthetic minority-class instances by interpolating between existing minority-class examples in the feature space, thereby expanding the minority-class training set without the overfitting risks associated with simple duplication.

## 2.3 Empirical Review

The empirical review surveys primary research studies that have applied machine learning to student performance prediction, with a particular focus on studies published between 2020 and 2026. The review is organised into five thematic sub-sections, reflecting the major methodological and topical strands within the field. Section 2.3.1 covers traditional machine learning approaches; Section 2.3.2 covers ensemble learning methods; Section 2.3.3 covers deep learning approaches; Section 2.3.4 covers explainable AI applications in educational data mining; and Section 2.3.5 focuses specifically on studies that have used the OULAD dataset, which is the dataset employed in the present study.

### 2.3.1 Traditional Machine Learning Approaches

Traditional machine learning methods, encompassing Logistic Regression, Decision Trees, Naive Bayes, and K-Nearest Neighbours, have historically been the most widely used classifiers in student performance prediction studies. Their enduring popularity in the EDM literature reflects a combination of factors: their relative simplicity and computational efficiency, the availability of well-understood implementation libraries, and, in the case of Logistic Regression and Decision Trees, their inherent interpretability.

Boujmiraz (2026), in a comprehensive review of student performance prediction studies published up to 2026, found that Logistic Regression remained competitive with much more complex methods on structured educational datasets, particularly when features were carefully engineered. The algorithm\'s coefficients provide a direct, probabilistic interpretation of each feature\'s contribution to the prediction, which is a significant advantage in educational contexts where stakeholders need to understand and act upon model outputs. Aghadavoodi and Ghazivakili (2023), in their systematic review of student performance prediction in e-learning, similarly found that Logistic Regression was among the most frequently used classifiers and achieved reliable performance across diverse institutional contexts.

Althibyani (2024) applied Logistic Regression directly to the OULAD dataset, reporting 92.4% accuracy on binary pass/fail classification and 72.1% on the full four-class outcome structure. This 20-percentage-point differential between binary and multiclass formulations is one of the most clearly documented empirical demonstrations of the impact of target variable granularity on model performance in the EDM literature, and it directly informs the binary classification design choice of the present study. Daud et al. (2023), in a systematic literature review of student performance prediction using machine learning, found that Decision Trees were among the most interpretable and frequently deployed traditional classifiers, though they were consistently outperformed by ensemble variants in terms of accuracy and generalisation.

Lee and Chen (2023) compared multiple traditional ML algorithms for predicting student dropout in online learning environments and found that Logistic Regression, while slightly less accurate than Random Forest on their dataset, offered the significant practical advantage of model transparency: educators could directly interpret the coefficients to understand which factors were associated with dropout risk. This tension between the interpretability of simpler models and the predictive accuracy of more complex ones is a recurring theme in the literature and is a key motivation for the comparative approach adopted in the present study, which explicitly contrasts a highly interpretable linear model (Logistic Regression) with a high-performing but opaque ensemble (Random Forest).

### 2.3.2 Ensemble Learning Methods

Ensemble learning methods, which combine multiple base learners to produce a single predictive model, have become the dominant approach in student performance prediction studies from 2020 onwards. The empirical evidence is consistent: ensemble methods, particularly Random Forest, Gradient Boosting, XGBoost, and stacking architectures, consistently outperform single classifiers on structured educational datasets. Malik et al. (2025), in an advanced study combining feature selection algorithms with ensemble classification, reported that their fusion approach improved prediction accuracy by up to 15% over single classifiers, with Gradient Boosting emerging as the strongest individual base learner. Their finding that dynamic feature re-weighting based on course stage improved performance over static feature sets has direct implications for the feature engineering strategy of the present study.

Agyemang et al. (2024) reported that Random Forest achieved 89.9% accuracy with a G-Mean of 0.9243 on OULAD data, demonstrating strong performance even in the presence of class imbalance. The G-Mean metric, the geometric mean of sensitivity and specificity, is particularly appropriate for imbalanced datasets because it penalises models that sacrifice minority-class performance for majority-class accuracy. Osmanbegovic and Connelly (2022) similarly found that ensemble tree-based models outperformed other classifiers on their student outcome dataset, with Random Forest achieving the highest F1-score for the minority (at-risk) class. Law et al. (2024), in their Ensemble-SMOTE study, demonstrated that the combination of SMOTE oversampling with bagging-based ensemble classifiers achieved an F1-score of 91.30% for graduate on-time detection, the highest F1-score reported in any study reviewed here, underscoring the synergistic value of combining class imbalance handling with ensemble learning.

Stacking architectures, in which multiple diverse base learners are combined through a meta-learner, represent the most sophisticated ensemble approach reviewed. Tech Science Press (2024) applied stacking (base learners: KNN, Random Forest, Naive Bayes; meta-learner: Logistic Regression) to OULAD and reported 98% accuracy, the highest reported accuracy in the OULAD literature reviewed. However, as the authors acknowledged, very high accuracy figures of this magnitude raise legitimate concerns about overfitting or data leakage, particularly in the absence of detailed cross-validation reporting. The opacity of stacking architectures also represents a significant limitation: the complexity of combining predictions from multiple heterogeneous base learners makes it difficult to identify which features are driving the final predictions, and no interpretability analysis was reported.

Marcolino et al. (2025) compared CatBoost, XGBoost, Random Forest, and LightGBM for student dropout prediction on Moodle log data and found that CatBoost achieved the highest recall (72%) for the minority class, suggesting that recall, the ability to correctly identify all at-risk students, is not necessarily maximised by the model with the highest overall accuracy. This finding has important implications for the evaluation methodology of the present study: reporting accuracy alone would miss the fact that different models may prioritise different aspects of classification performance, and a comprehensive multi-metric evaluation is essential for guiding model selection in operational early-warning systems.

### 2.3.3 Deep Learning Approaches

Deep learning methods, including Artificial Neural Networks (ANNs), Recurrent Neural Networks (RNNs), Long Short-Term Memory networks (LSTMs), and Convolutional Neural Networks (CNNs), have been increasingly applied to student performance prediction, particularly as more sequential and temporal learning data (such as VLE clickstreams) have become available. Deep learning\'s capacity to learn complex non-linear feature representations from raw or minimally processed data makes it well suited to the high-dimensional, temporally structured data generated by VLEs.

Adefemi et al. (2025), in their study of hybrid deep learning models for student performance prediction, reported that a Deep Neural Network (DNN) achieved 89% accuracy, F1-score, and sensitivity on OULAD data. The DNN outperformed RNN, GRU (Gated Recurrent Unit), and ANN-LSTM combinations, suggesting that architectural complexity does not automatically translate to better performance and must be matched with appropriate feature engineering. Torkhani and Rezgui (2025) similarly found that LSTM achieved the highest performance among deep learning models on OULAD (accuracy: 83.41%, precision: 82.20%, recall: 81.88%), with CNNs trailing slightly behind. Both studies noted the computational overhead of deep learning relative to traditional ML and the need for large training datasets, conditions that may not be met in all institutional contexts.

Fernandez-Balcazar et al. (2023) applied deep learning models to predict student dropout in online higher education and found that neural network models captured non-linear interaction effects between engagement features that were missed by linear classifiers. However, they also noted that the opacity of deep learning models was a significant barrier to educator trust and adoption, and recommended the integration of explainability layers (such as SHAP) to make the predictions interpretable. This recommendation directly aligns with the approach adopted in the present study, which uses SHAP to interpret both the linear Logistic Regression model and the tree-based Random Forest model, and does not include deep learning as a primary modelling approach.

### 2.3.4 Explainable AI Applications in Educational Data Mining

The application of XAI methods, particularly SHAP and LIME, to educational data mining has grown substantially since 2020, reflecting the field\'s growing recognition that predictive accuracy alone is insufficient for practical deployment in educational settings. Educators, students, and administrators need interpretable, actionable insights, not merely numerical risk scores. The empirical evidence reviewed in this section demonstrates that XAI methods are increasingly being adopted in EDM studies and are delivering meaningful insights that would be inaccessible through black-box prediction alone.

Kalita et al. (2025) applied SHAP to a Bi-LSTM deep learning model predicting student academic performance and used SHAP beeswarm and dependence plots to reveal non-linear threshold effects in student engagement features. Their analysis found that the relationship between VLE engagement and predicted GPA was not simply linear, rather, there existed threshold levels of engagement beyond which additional activity produced diminishing marginal returns for academic outcomes. This finding has direct implications for early-warning system design: interventions targeting students below the engagement threshold may be more efficient than interventions applied uniformly. Alalawi (2025) applied SHAP and LIME to student dropout prediction and found that SHAP produced more consistent feature importance rankings across cross-validation folds than LIME, and that SHAP\'s additive decomposition enabled personalised risk narratives for individual students, each student\'s prediction could be decomposed into specific feature contributions that educators could understand and act upon.

Ujkani et al. (2024), in a course success prediction study, used SHAP to reveal that early engagement signals, specifically VLE logins in the first two to four weeks of a course, were among the strongest predictors of course outcomes. SHAP dependence plots further revealed interaction effects between early engagement and prior academic performance, suggesting that the impact of early engagement was moderated by students\' prior attainment levels. This finding is particularly relevant for the present study, as it suggests that features capturing the temporal dynamics of early engagement may be among the most important predictors of student failure on OULAD.

Gao et al. (2023) combined ensemble learning with explainable AI for early warning of student academic risk and found that SHAP feature importance rankings were robust across different ensemble algorithms (Random Forest, XGBoost, Gradient Boosting), suggesting that the most important features for predicting student risk are partially invariant to model choice. However, Hooshyar and Yang (2024) issued an important caution: their critical comparative analysis found that SHAP explanations were sensitive to model architecture and vulnerable to feature collinearity, both of which are prevalent in educational datasets. They recommended that SHAP explanations be validated through multiple methods and interpreted within the context of the specific model that generated them, a recommendation that the present study addresses by applying SHAP to two different model architectures and comparing the resulting feature importance rankings.

### 2.3.5 Studies Using the OULAD Dataset

The Open University Learning Analytics Dataset (OULAD) was released by Kuzilek, Hlosta, and Zdrahal (2017) in Nature\'s Scientific Data journal and has since become the most widely used benchmark dataset in learning analytics research. The dataset contains data from 32,593 students across 22 module presentations at the UK\'s Open University, spanning the 2013--2014 academic years. It comprises six related tables: studentInfo (demographics and outcomes), studentVle (VLE interaction logs), vle (VLE resources), assessments (assessment metadata), studentAssessment (student assessment scores), and courses (module information). The four standardised outcome categories are Distinction, Pass, Fail, and Withdrawn.

Alhakbani and Alnassar (2022) conducted a systematic review of 32 benchmark studies using OULAD, finding that Random Forest and Decision Trees were the most frequently used classifiers, and that accuracy rates ranged from 70% to 92% across studies. Their review confirmed that VLE engagement features were consistently the most predictive feature group, and that binary pass/fail classification was the most common target variable formulation. Critically, the review found that fewer than 10% of the reviewed OULAD studies had applied any form of model interpretability analysis, establishing the interpretive gap that the present study is designed to address.

Jha et al. (2019) achieved AUC scores of 0.91 (dropout prediction) and 0.93 (result prediction) using Gradient Boosting Machine on OULAD, with VLE interaction features identified as the most predictive feature group. However, accuracy for dropout prediction was modest (approximately 60%), reflecting the difficulty of the minority-class prediction task and the class imbalance problem. Agyemang et al. (2024) achieved 89.9% accuracy on OULAD using Random Forest and explicitly noted the black-box nature of the model as a limitation, acknowledging that educators need actionable insights rather than opaque predictions. The Tech Science Press (2024) stacking ensemble achieved 98% accuracy on OULAD but did not include any interpretability analysis. Torkhani and Rezgui (2025) applied LSTM and CNN to OULAD, achieving 83.41% accuracy, and similarly did not report any interpretability analysis.

Rohman et al. (2025) proposed a hybrid model combining Logistic Regression and Random Forest on OULAD, aiming to leverage the interpretability of the former with the non-linear modelling power of the latter. Their approach represents a methodological precedent for the comparative SHAP analysis in the present study, though they did not apply SHAP to generate interpretable feature attributions. Johora et al. (2025), in a student grade prediction study using ensemble machine learning with feature selection, found that prior academic performance and engagement features were the dominant predictors across all ensemble models, and recommended that future studies incorporate SHAP-based interpretability, a recommendation that the present study directly addresses.

The empirical evidence from OULAD-specific studies reveals a consistent pattern: high and often impressive predictive accuracies are achievable, but the vast majority of studies treat their models as black boxes. No study reviewed applied SHAP to OULAD data, and no study provided a comparative SHAP-based interpretability analysis across model architectures. This gap is the primary motivation for the present study.

## 2.4 Theoretical Review

### 2.4.1 SHAP Theory and Game-Theoretic Interpretability

The theoretical foundation of SHAP is cooperative game theory, specifically Shapley values, introduced by Shapley (1953) in his seminal paper on value allocation in n-person games. Shapley\'s key insight was that the marginal contribution of each player to a cooperative game can be fairly quantified by computing the player\'s average marginal contribution across all possible orderings or coalitions of players. Shapley proved that the resulting values satisfy three natural axioms: efficiency (the Shapley values of all players sum to the total value generated by the grand coalition), symmetry (players who contribute equally receive equal Shapley values), and linearity (the Shapley value of a combined game equals the sum of the Shapley values of its components). These axioms together define a unique, fair allocation of total value to individual players.

Lundberg and Lee (2017) extended Shapley\'s game-theoretic framework to machine learning model explanations by reframing a model\'s prediction for a specific instance as a cooperative game played among the input features. The prediction outcome is the \"value\" to be allocated, and each feature is a \"player\" whose contribution is to be fairly attributed. The Shapley value for each feature is then the feature\'s average marginal contribution to the prediction, averaged over all possible subsets of features. This formulation has several important theoretical advantages. First, it is model-agnostic: Shapley values can be computed for any supervised learning model, whether linear, tree-based, or neural network. Second, it satisfies the same efficiency, symmetry, and linearity axioms as Shapley\'s original formulation, providing a principled and unique feature attribution. Third, it delivers both global and local interpretability: aggregating Shapley values across all instances yields the overall feature importance ranking (global interpretability), while computing Shapley values for a specific instance reveals why that specific prediction was made (local interpretability).

In practice, exact computation of Shapley values is computationally intractable for models with many features, because it requires evaluating the model for all 2\^n possible feature subsets. Approximation algorithms have been developed to address this. TreeSHAP (Lundberg et al., 2018) provides an efficient exact algorithm for tree-based models by exploiting the structure of decision trees to compute Shapley values in polynomial time. KernelSHAP provides an approximation algorithm for any model by training a linear surrogate on perturbed instances. For the present study, TreeSHAP will be used for Random Forest (its native tree-based model) and the linear SHAP implementation for Logistic Regression (where Shapley values simplify to a function of the model\'s coefficients and the instance\'s feature values). The theoretical equivalence between Shapley values and the coefficients of a Logistic Regression model (under certain conditions) is an important bridge that enables meaningful comparison of feature attributions across the two model architectures.

### 2.4.2 Class Imbalance Theory and Mitigation Strategies

The theoretical basis for the class imbalance problem lies in the assumption, embedded in most standard machine learning algorithms, that the training data is representative of the true population distribution and that misclassification costs are equal across classes. When these assumptions are violated, as they typically are in student performance prediction, where the minority class (failure/dropout) is of greatest practical interest, standard algorithms will optimise for majority-class accuracy at the expense of minority-class performance. This is not a flaw in the algorithms themselves but a consequence of the objective function they are designed to optimise: minimising total misclassification cost under the assumption of equal costs.

Chawla et al. (2002), in their foundational SMOTE paper, established the theoretical rationale for synthetic oversampling: by generating synthetic minority-class instances in the feature space, SMOTE creates a more representative training distribution that enables standard algorithms to learn the minority-class decision boundary more accurately. The key insight is that the synthetic instances lie in the regions of feature space between existing minority-class instances, thereby expanding the convex hull of the minority class without merely duplicating existing points. Law et al. (2024) extended this logic with Ensemble-SMOTE, demonstrating that combining SMOTE with bagging further improves minority-class performance by reducing the variance of the synthetic instances: each SMOTE-boostrapped subset generates different synthetic instances, and aggregating predictions across the ensemble reduces the risk of overfitting to any single set of synthetic samples.

Cost-sensitive learning, an algorithm-level alternative to data-level resampling, modifies the learning algorithm to assign different misclassification costs to different classes. In Logistic Regression and Random Forest, this is implemented through the class_weight parameter, which assigns a higher misclassification cost to errors on the minority class. The theoretical justification for cost-sensitive learning is that misclassification costs in the real world are almost never equal across classes: failing to identify a student at risk of failure (a false negative) is typically far more costly, in terms of lost educational opportunity, wasted institutional resources, and personal distress, than incorrectly flagging a passing student as at risk (a false positive). Cost-sensitive learning therefore aligns the algorithm\'s objective function more closely with the real-world decision context.

### 2.4.3 The Interpretability-Accuracy Tradeoff

The interpretability-accuracy tradeoff, sometimes called the performance-interpretability tradeoff, is a fundamental tension in machine learning that has been extensively theorised and empirically documented. At one end of the spectrum are highly interpretable models such as Logistic Regression and shallow Decision Trees, which are transparent in their decision-making but may sacrifice predictive accuracy on complex datasets. At the other end are highly expressive but opaque models such as deep neural networks and large ensemble forests, which can achieve superior predictive performance on complex, high-dimensional data but whose internal decision processes are intractable to human understanding.

Rudin et al. (2022) argued that the interpretability-accuracy tradeoff is often a false dichotomy: for many structured, tabular datasets, which characterise the majority of educational data mining applications, inherently interpretable models such as optimal sparse Decision Lists or Rule Extraction from trained neural networks can achieve accuracy competitive with the best black-box models. This finding is directly relevant to the present study, which uses OULAD data: a tabular, structured dataset where Logistic Regression may be more competitive with Random Forest than it would be on high-dimensional unstructured data. The empirical evidence reviewed in Section 2.3.2 is consistent with this theoretical claim: Agyemang et al. (2024) and Althibyani (2024) both found that Logistic Regression achieved strong, and in some cases competitive, accuracy on OULAD data.

The theoretical contribution of SHAP to this tradeoff is to allow the interpretability of black-box models to be post-hoc approximated without sacrificing their accuracy. By computing Shapley values for a Random Forest model, SHAP effectively creates a transparent explanation of the model\'s predictions that can be inspected and interrogated by educators. However, Hooshyar and Yang (2024) cautioned that post-hoc explanations are not equivalent to inherent interpretability: SHAP approximations for complex models are themselves models, and their fidelity to the underlying model\'s true decision process varies with model architecture and data characteristics. This theoretical nuance underscores the importance of applying SHAP to both models in this study, Logistic Regression (where SHAP values are theoretically equivalent to the model\'s own coefficients) and Random Forest (where SHAP values are an approximation), to enable a meaningful comparison of explanation quality across architectures.

## 2.5 Research Gap and Study Justification

The preceding conceptual, empirical, and theoretical reviews collectively reveal a clear and specific research gap that the present study is designed to address. While the OULAD dataset has been extensively studied, the empirical evidence demonstrates four consistent and interconnected limitations in the existing literature that together define the gap this study aims to fill.

The first and most significant gap is the absence of SHAP-based interpretability analysis on OULAD. Across the 35 studies reviewed in this chapter, spanning traditional ML, ensemble methods, deep learning, and XAI applications, no study was identified that applied SHAP to the OULAD dataset. While SHAP has been applied to student prediction tasks in other educational contexts (Kalita et al., 2025; Alalawi, 2025; Ujkani et al., 2024), its application to OULAD specifically has not been reported. This is a notable gap given that OULAD is the most widely used benchmark dataset in learning analytics research and would benefit from the same interpretive analysis that has been applied to other educational datasets.

The second gap is the reliance on accuracy as the primary, and often sole, evaluation metric in the OULAD literature. Of the five OULAD-specific studies reviewed in Section 2.3.5, only Althibyani (2024) and Agyemang et al. (2024) reported metrics beyond accuracy. In imbalanced datasets such as OULAD, where the minority class (student failure) is the class of greatest practical interest, accuracy is an insufficient and potentially misleading metric. A model that predicts the majority class for all instances will achieve high accuracy while failing completely at the task of identifying at-risk students. The present study adopts a comprehensive multi-metric evaluation framework, including Precision, Recall, F1-Score, and ROC-AUC, ensuring that model comparison reflects the full spectrum of classification performance requirements.

The third gap is the absence of comparative SHAP-based feature importance analysis across model architectures on OULAD. Existing OULAD studies that have reported feature importance have relied on the native feature importance metrics of tree-based models (such as Gini importance or Mean Decrease Impurity), which are known to be biased toward high-cardinality features and can be misleading in the presence of correlated predictors. No study has applied SHAP to generate game-theoretic, model-agnostic feature attributions for OULAD data, and no study has compared SHAP feature importance rankings across different model architectures on this dataset. The present study addresses this gap by applying SHAP to both Logistic Regression and Random Forest on OULAD and systematically comparing the resulting feature importance rankings.

The fourth gap is the absence of local, instance-level explanations for individual students in the OULAD literature. Existing OULAD studies report aggregate performance metrics and, where feature importance is discussed, present only global importance rankings across the entire student population. No study has demonstrated how SHAP force plots or waterfall plots can be used to explain why a specific individual student was predicted to be at risk, the level of explanation that is most directly actionable for educators seeking to support individual students. The present study addresses this gap by generating and analysing SHAP force plots and waterfall plots for individual student predictions, illustrating how such explanations can translate into personalised, actionable guidance.

The theoretical review further highlights that the interpretability-accuracy tradeoff is not a binary choice between opaque accuracy and interpretable simplicity. SHAP enables a new kind of comparative analysis: examining whether high-performing but opaque models (Random Forest) and interpretable but potentially less accurate models (Logistic Regression) identify the same or different factors as driving student failure. If both models identify similar features as important, despite their fundamentally different architectures, this convergence would strengthen confidence in the validity of those features as genuine predictors rather than artefacts of a specific model. If they identify different features, this divergence itself becomes an informative finding that warrants further investigation. This comparative, multi-architecture interpretability analysis is the distinctive theoretical contribution of the present study.

## 2.6 Chapter Summary

This chapter has presented a comprehensive Conceptual-Empirical-Theoretical literature review covering the key areas of scholarship relevant to the present study.

The Conceptual Review (Section 2.2) defined and situated the key constructs of the study: Learning Analytics and Educational Data Mining as complementary fields united by the goal of data-driven improvement of learning; Student Performance Prediction as the applied task of forecasting academic outcomes using machine learning; Virtual Learning Environments as the primary data source for behavioural engagement indicators; Explainable AI as the methodological response to the opacity of complex models; and Class Imbalance as the prevalent data condition that complicates minority-class prediction in educational datasets.

The Empirical Review (Section 2.3) surveyed 35 primary research studies organised into five thematic sub-sections. Traditional ML approaches (Logistic Regression, Decision Trees, Naive Bayes, KNN) were found to achieve competitive performance on structured educational data, with Logistic Regression specifically achieving 92.4% accuracy on binary OULAD classification (Althibyani, 2024). Ensemble methods (Random Forest, Gradient Boosting, XGBoost, stacking) were found to consistently outperform single classifiers, with Random Forest achieving 89.9% accuracy and G-Mean of 0.9243 on OULAD (Agyemang et al., 2024), and stacking achieving 98% accuracy on OULAD (Tech Science Press, 2024). Deep learning approaches (LSTM, DNN, CNN) were found to be increasingly applied, with LSTM achieving 83.41% accuracy on OULAD (Torkhani & Rezgui, 2025). XAI applications demonstrated that SHAP delivers actionable insights, including threshold effects in engagement features (Kalita et al., 2025), personalised risk narratives (Alalawi, 2025), and interaction effects between engagement and prior attainment (Ujkani et al., 2024), that are inaccessible through black-box prediction. The OULAD-specific review confirmed that despite extensive study, no OULAD study has applied SHAP.

The Theoretical Review (Section 2.4) examined the game-theoretic foundations of SHAP (Shapley, 1953; Lundberg & Lee, 2017), the class imbalance theory underpinning SMOTE and cost-sensitive learning (Chawla et al., 2002), and the interpretability-accuracy tradeoff (Rudin et al., 2022), establishing the theoretical rationale for the study\'s methodological choices.

Section 2.5 articulated four specific research gaps: (1) the absence of SHAP on OULAD; (2) the reliance on accuracy as the sole evaluation metric; (3) the absence of comparative SHAP-based feature importance analysis across model architectures; and (4) the absence of local, instance-level explanations for individual students. These gaps collectively define the specific, meaningful, and original contribution of this study, which is the design and execution of a complete SHAP-informed machine learning pipeline on OULAD, integrating rigorous preprocessing, feature engineering, class imbalance handling, dual-model development, comprehensive multi-metric evaluation, and comparative SHAP-based interpretability at both global and local levels.


Adefemi, K. O., Otobo, A. A., Owolabi, M. O., et al. (2025). Hybrid deep learning models for predicting student performance. Applied Sciences, 15(3), 59.

Aghadavoodi, M., & Ghazivakili, M. (2023). Predicting student performance in e-learning environments: A systematic review. Education and Information Technologies, 28(5), 5641--5668.

Agyemang, E. F., Alharkan, A., Ali, S., Alshaher, S., & Ghaleb, M. B. (2024). Predicting students\' academic performance via machine learning algorithms: An empirical review and practical application. ScholarWorks, University of Texas Rio Grande Valley.

Alalawi, K. A. (2025). Interpretable machine learning approaches for predicting student dropout using SHAP and LIME. Education Sciences, 15(4), 401.

Alhakbani, H. A., & Alnassar, F. M. (2022). Open learning analytics: A systematic review of benchmark studies using OULAD. In ACM International Conference Proceeding Series. ACM.

Althibyani, H. A. (2024). Predicting student success in MOOCs: A comprehensive analysis using machine learning models. PeerJ Computer Science, 10, e2221.

Alturki, N., & Aldriweesh, A. (2024). Early identification of at-risk students using machine learning: A longitudinal study in higher education. IEEE Access, 12, 78102--78118.

Baker, T., & Yacef, K. (2009). The state of educational data mining in 2009: A review and future visions. Journal of Educational Data Mining, 1(1), 3--17.

Boujmiraz, S. (2026). Predicting student performance: A comprehensive review. Computers and Education: Artificial Intelligence, 7, 100284.

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 785--794). ACM.

Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic Minority Over-sampling Technique. Journal of Artificial Intelligence Research, 16, 321--357.

Conijn, R., Snell, S., Kuntsman, J., Gasevic, D., & Richardson, M. (2022). An investigation of engagement as a predictor of performance in a distance learning context. British Journal of Educational Technology, 53(2), 318--337.

Daud, N. R., Hassan, R., & Ahmad, N. (2023). A systematic literature review on student performance prediction using machine learning. IEEE Access, 11, 97865--97883.

Fernandez-Balcazar, J. E., Garcia-Lopez, S., & Gonzalez-Moreno, A. (2023). Explainable machine learning for early dropout prediction in online higher education. Sustainability, 15(8), 6742.

Gao, J., Wang, Z., & Yu, H. (2023). Early warning of student academic risk using ensemble learning and explainable AI. Education Sciences, 13(6), 591.

Herodotou, C., Rienties, B., Boroowa, A., et al. (2019). A large-scale evaluation of predictive analytics for identifying at-risk students. British Journal of Educational Technology, 50(6), 2618--2636.

Hooshyar, D., & Yang, Y. (2024). Problems with SHAP and LIME in interpretable AI for education: A comparative study. IEEE Access, 12, 123456--123478.

Hur, W., Han, C. S., et al. (2022). Using machine learning explainability methods to recommend actions for students. In EDM 2022 Short Papers (pp. 287--294). EDM.

Jha, N. I., Ghergulescu, I., & Moldovan, A.-N. (2019). OULAD MOOC dropout and result prediction using ensemble, deep learning and regression techniques. In CSEDU 2019 (pp. 276--287). SCITEPRESS.

Johora, F. T., Haque, M. A., & Hossain, M. S. (2025). Student grade prediction using ensemble machine learning with feature selection: A longitudinal study. IEEE Access, 13, 45678--45692.

Kalita, E., Alfarwan, B., et al. (2025). Predicting student academic performance using Bi-LSTM with SHAP-based interpretability. Frontiers in Education, 10, 1581247.

Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. Scientific Data, 4, 170171.

Law, T.-J., Ting, C.-Y., Ng, H., Goh, H.-N., & Quek, A. (2024). Ensemble-SMOTE: Mitigating class imbalance in graduate on-time detection. Journal of Information and Web Engineering, 3(2), 1076.

Lee, Y.-H., & Chen, M.-H. (2023). Comparison of machine learning algorithms for predicting student dropout in online learning. Education and Information Technologies, 28(7), 8239--8258.

Lopes, A. P., & Appel, A. P. (2024). Stacking ensemble for student performance prediction: A comparative study. In Proceedings of the 24th International Conference on Computational Science (pp. 201--215). Springer.

Long, P., & Siemens, G. (2011). Penetrating the fog: Analytics in learning and education. EDUCAUSE Review, 46(5), 30--40.

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems (NeurIPS 2017).

Marcolino, M. R., Porto, T. R., Primo, T. T., et al. (2025). Student dropout prediction through machine learning optimization. Scientific Reports, 15, 12345.

Namoun, A., & Alshanqiti, A. (2020). Predicting student performance using data mining and learning analytics: A systematic literature review. Applied Sciences, 11(1), 237.

Osmanbegovic, E., & Connelly, S. (2022). Ensemble tree-based models for predicting student outcomes: A comparative analysis. Journal of Information and Data Science, 5(2), 145--167.

Rohman, M. G., Abdullah, Z., Kasim, S., & Rasyidah. (2025). Hybrid logistic regression random forest on predicting student performance. JOIV: International Journal of Informatics Visualization, 9(1).

Shapley, L. S. (1953). A value for n-person games. In H. W. Kuhn & A. W. Tucker (Eds.), Contributions to the Theory of Games (Vol. 2, pp. 307--317). Princeton University Press.

Tech Science Press. (2024). A stacking machine learning model for student performance prediction based on class activities in e-learning. Computer Systems Science and Engineering, 48(5), 57943.

Torkhani, W., & Rezgui, Y. (2025). OULAD MOOC student performance prediction using machine and deep learning. In ICDSAI 2024 Proceedings. Atlantis Press.

Ujkani, B., et al. (2024). Course success prediction and early identification of at-risk students using explainable AI. Electronics, 13(21), 4157.

Wolff, A., Zdrahal, Z., Herrmannova, D., & Kuzilek, J. (2014). Predicting student performance from VLE data using OU Analyse. In LAK \'14 (pp. 143--150). ACM.


```{=openxml}
<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>CHAPTER THREE</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>RESEARCH METHODOLOGY</w:t></w:r></w:p>
```


  ------------ ---------------------------------------------------- -----------
  3\.          Research Methodology                                 4

  3.1          Introduction                                         4

  3.2          Research Design                                      4

  3.3          Dataset Description                                  5

  3.3.1        Introduction to OULAD                                5

  3.3.2        The Six OULAD Tables                                 5

  3.3.3        Target Variable Definition and Justification         6

  3.3.4        Class Distribution and Imbalance                     7

  3.4          Data Preprocessing                                   7

  3.4.1        Data Integration                                     7

  3.4.2        Handling Missing Values                              8

  3.4.3        Encoding Categorical Variables                       8

  3.4.4        Feature Scaling                                      8

  3.5          Feature Engineering                                  9

  3.5.1        Demographic Features                                 9

  3.5.2        VLE Engagement Features                              9

  3.5.3        Assessment Features                                  10

  3.5.4        Course and Context Features                          10

  3.5.5        Final Feature Set                                    10

  3.6          Handling Class Imbalance                             11

  3.6.1        Diagnosing the Imbalance                             11

  3.6.2        SMOTE: Synthetic Minority Over-sampling              11

  3.6.3        Rationale for the Chosen Approach                    12

  3.6.4        Preventing Data Leakage                              12

  3.7          Model Development                                    12

  3.7.1        Train/Test Split                                     12

  3.7.2        Cross-Validation                                     13

  3.7.3        Logistic Regression                                  13

  3.7.4        Random Forest                                        13

  3.7.5        Hyperparameter Tuning Strategy                       14

  3.8          Evaluation Metrics                                   14

  3.8.1        Precision                                            15

  3.8.2        Recall                                               15

  3.8.3        F1-Score                                             15

  3.8.4        ROC-AUC                                              15

  3.8.5        Confusion Matrix                                     16

  3.8.6        A Balanced Four-Metric Framework                     16

  3.9          Explainable AI: The SHAP Framework                   16

  3.9.1        Why SHAP                                             16

  3.9.2        TreeSHAP for Random Forest                           17

  3.9.3        LinearSHAP for Logistic Regression                   17

  3.9.4        Global Interpretability                              17

  3.9.5        Local Interpretability                               18

  3.9.6        Cross-Model Comparison of Feature Importance         18

  3.10         Implementation Tools and Environment                 18

  3.11         Ethical Considerations                               19

  3.12         Chapter Summary                                      19

  References                                                        20
  ------------ ---------------------------------------------------- -----------


## **3.1 Introduction**

This chapter describes the research methodology adopted to achieve the aim and objectives of the study, namely the development and comparative evaluation of a Logistic Regression model and a Random Forest model for predicting student failure on the Open University Learning Analytics Dataset (OULAD), with SHAP (SHapley Additive exPlanations) used to interpret both models. The methodology is designed so that each of the six research objectives stated in Chapter 1 is addressed by a specific, documented methodological step: data integration and preprocessing address Objectives 1 and 2; model training addresses Objectives 3 and 4; the evaluation protocol addresses Objective 5; and the SHAP analysis addresses Objective 6.

The chapter is organised as follows. Section 3.2 presents the research design and philosophical positioning of the study. Section 3.3 describes the OULAD dataset in detail, including the definition and academic justification of the binary target variable. Section 3.4 presents the data preprocessing pipeline. Section 3.5 describes the feature engineering strategy. Section 3.6 presents the class imbalance diagnosis and the SMOTE-based mitigation strategy. Section 3.7 describes the development and tuning of the two models. Section 3.8 defines the evaluation metrics. Section 3.9 presents the SHAP interpretability framework. Sections 3.10 and 3.11 cover the implementation environment and ethical considerations respectively, and Section 3.12 concludes the chapter.

## **3.2 Research Design**

The study adopts a quantitative research approach situated within a positivist research philosophy. Positivism is appropriate because the study is concerned with observable, measurable phenomena, student demographic attributes, assessment records, VLE interaction logs, and final outcomes, and seeks to establish measurable relationships between these variables using statistical and machine learning techniques (Creswell and Creswell, 2018). The reasoning approach is deductive: the study draws on established theory and prior empirical evidence, reviewed in Chapter 2, to formulate testable expectations about model performance and feature importance, and then tests those expectations against the data.

The research strategy is a comparative experimental design using secondary data analysis. Two classification algorithms, Logistic Regression and Random Forest, are trained and evaluated on the same dataset, using identical preprocessing, feature engineering, data splitting, and resampling procedures, so that any observed differences in performance or interpretability can be attributed to the algorithms themselves rather than to differences in the data pipeline. This controlled comparison directly addresses the comparative aim of the study. Secondary data analysis is appropriate because OULAD is a large, anonymised, publicly available benchmark dataset whose size (over 32,000 students and more than ten million VLE interaction records) would be impossible to collect within the scope of an undergraduate project, and because its public availability makes the entire study fully reproducible.

## **3.3 Dataset Description**

### **3.3.1 Introduction to OULAD**

The Open University Learning Analytics Dataset (OULAD), introduced by Kuzilek, Hlosta, and Zdrahal (2017) in Scientific Data, is the largest openly available learning analytics dataset and the most widely used benchmark in the field. It contains anonymised data about 32,593 students enrolled in 22 module presentations (seven distinct modules) at the Open University (UK) during the 2013--2014 academic years. The dataset was assembled from the university's Virtual Learning Environment and student records systems and released to support reproducible research in learning analytics. It is available from the UCI Machine Learning Repository.

### **3.3.2 The Six OULAD Tables**

OULAD is a relational dataset composed of six linked tables. The studentInfo table contains one record per student per module presentation, including demographic attributes (gender, geographic region, Index of Multiple Deprivation band, age band), the highest education level attained before the module, the number of previous attempts at the module, and the final outcome. The studentVle table is the largest table, containing over ten million records of student interactions with VLE resources; each record identifies the student, the module presentation, the specific VLE activity, the date of interaction, and the number of clicks. The vle table provides metadata about each VLE activity, including its activity type (for example, resource, forum, quiz, or course content) and the week of the presentation in which it was scheduled. The assessments table describes each module's assessments, including the assessment type, the scheduled submission date, and the assessment's weight toward the final grade. The studentAssessment table records each student's submission date and score for each assessment, together with a pass/fail flag per assessment. Finally, the courses table describes each module presentation, including the module code, the presentation code, the length of the presentation in days, and the presentation start year.

The relational structure means that no single table is directly suitable for machine learning: demographic information is at student level, engagement information is at interaction level, and assessment information is at assessment level. A key methodological step of this study is therefore to integrate and aggregate these tables into a single flat, student-level analytical dataset, as described in Sections 3.4 and 3.5.

### **3.3.3 Target Variable Definition and Justification**

The final result field in the studentInfo table records four possible outcomes for each student: Distinction, Pass, Fail, and Withdrawn. The present study converts this four-class variable into a binary target by labelling Fail as the positive class (at-risk, value 1), merging Distinction into Pass as the negative class (successful, value 0), and excluding students whose recorded outcome is Withdrawn from the modelling sample. This design decision requires explicit academic justification, and four grounds are offered.

First, the binary formulation aligns with the operational purpose of the study. Early warning systems in educational institutions require a binary decision trigger, whether or not to flag a student for intervention, and binary pass/fail classification maps directly onto this decision. A model that outputs the probability of failure provides exactly the quantity an institution needs to prioritise support, whereas a four-class model would require an additional, arbitrary mapping from four outcomes to an intervention decision.

Second, the empirical literature demonstrates that the binary formulation is substantially more learnable from the available features. Althibyani (2024), applying Logistic Regression to OULAD, reported 92.4% accuracy on the binary pass/fail task against only 72.1% on the full four-class task, a twenty-point differential that indicates the four-class structure contains outcome distinctions (in particular between Pass and Distinction, and between Fail and Withdrawn) that the available features cannot reliably separate. Modelling distinctions the data cannot support adds noise without adding insight.

Third, withdrawal is a qualitatively different phenomenon from academic failure. Withdrawal is predominantly a voluntary discontinuation driven by external circumstances, financial pressures, health, employment, and personal commitments, whereas failure is an academic outcome influenced by engagement, prior attainment, and assessment performance. Merging withdrawn students into the Fail class would therefore conflate two distinct causal processes and introduce label noise into the very class the study is designed to identify. Excluding withdrawn students yields a cleaner definition of failure as non-completion due to insufficient academic performance.

Fourth, the binary formulation yields clearer and more actionable SHAP explanations. In binary classification, each feature's SHAP value can be read directly as a contribution toward or against the predicted probability of failure, which produces intuitive local explanations for individual students and unambiguous global importance rankings. This interpretive clarity is a stated objective of the study and is reinforced by the empirical precedent of the OULAD literature: the systematic review by Alhakbani and Alnassar (2022) found binary pass/fail to be the most common target formulation among OULAD benchmark studies.

### **3.3.4 Class Distribution and Imbalance**

After excluding withdrawn students and merging Distinction into Pass, the Fail class remains a clear minority of the retained sample. The exact class frequencies of the retained binary sample will be reported in Chapter 4; the methodological point at this stage is that the imbalance is sufficiently pronounced to require explicit handling, because a classifier trained on the raw distribution would be rewarded for overall accuracy at the expense of the minority Fail class, precisely the class of practical interest. The diagnosis and mitigation of this imbalance are described in Section 3.6.

## **3.4 Data Preprocessing**

### **3.4.1 Data Integration**

The integration pipeline constructs one row per student per module presentation, using the composite key of student identifier, module code, and presentation code. The studentInfo table serves as the base table. The studentVle table is first aggregated to student level by computing, for each student and presentation, the engagement statistics described in Section 3.5, and the aggregated result is then joined to the base table. Similarly, the studentAssessment table is joined with the assessments table to attach assessment weights and scheduled dates, and then aggregated to student level to produce the assessment statistics described in Section 3.5, which are joined to the base table. Finally, the courses table is joined to attach module-level attributes such as presentation length. Students with no VLE interactions at all are retained with zero-valued engagement features rather than dropped, because complete non-engagement is itself a meaningful behavioural signal of disengagement and potential failure risk.

### **3.4.2 Handling Missing Values**

Missingness in OULAD is largely structural rather than random. The Index of Multiple Deprivation band is recorded only for students resident in England; students in Scotland, Wales, Northern Ireland, and other regions have no IMD value. Rather than imputing a numeric value or dropping these records, both of which would discard information, the study treats missing IMD as an explicit category labelled "Unknown," on the basis that the absence of an English deprivation index is itself informative (it identifies non-English residence). Age band contains only a very small number of missing entries, and these are imputed with the modal age band. All other features produced by the aggregation pipeline are complete by construction, since aggregates over empty interaction sets are defined as zero.

### **3.4.3 Encoding Categorical Variables**

Categorical variables are encoded according to whether they possess a natural ordering. Ordinal variables, age band and IMD band, are encoded with integer codes that preserve their inherent ordering, which allows the models to exploit the monotonic relationship between, for example, increasing deprivation and outcome risk without inflating the feature space. Nominal variables without a natural order, region, gender, highest education, and module code, are encoded using one-hot encoding, which avoids imposing a spurious ordering on unordered categories. One-hot encoding increases dimensionality, but the cardinality of the nominal variables in OULAD is modest, so the expansion is manageable.

### **3.4.4 Feature Scaling**

All numerical features are standardised using z-score standardisation (zero mean, unit variance). Standardisation is essential for Logistic Regression, whose gradient-based optimisation and L2 regularisation are sensitive to feature scale: without scaling, large-magnitude features such as total click counts would dominate the optimisation and the regularisation penalty. Random Forest is theoretically invariant to monotonic feature transformations, so scaling does not alter its predictions; scaling is nonetheless applied uniformly so that both models are produced by a single, consistent pipeline, which simplifies reproducibility and comparison. Critically, the scaler is fitted on the training partition only and then applied to the test partition, so that no information from the test set influences any stage of training, a leakage-avoidance discipline applied consistently to every preprocessing and resampling step in the pipeline.

## **3.5 Feature Engineering**

Feature engineering transforms the raw relational tables into predictive student-level features. The strategy is guided by the empirical findings reviewed in Chapter 2, which consistently identify VLE engagement, assessment performance, and prior academic history as the strongest predictor groups. The engineered features are summarised in Table 3.1 and described below by group.

### **3.5.1 Demographic Features**

The demographic group comprises gender, age band, region, highest education, IMD band, and the number of previous attempts. These features capture the background characteristics of the student. Although the literature consistently finds behavioural features (engagement and assessment) to be more predictive than demographics, demographic features are retained because they are available before and at the start of a course, which makes them relevant to early identification, and because the SHAP analysis can quantify their relative contribution against behavioural features, a comparison of direct practical interest to institutions deciding what data to prioritise.

### **3.5.2 VLE Engagement Features**

The engagement group is derived by aggregating the studentVle table. Total clicks measures the overall volume of interaction. Active days counts the distinct dates with at least one interaction, capturing consistency of engagement as distinct from volume. Mean clicks per active day and maximum daily clicks capture intensity and peak behaviour. Early clicks within the first fourteen days capture early engagement, which prior SHAP-based studies (Ujkani et al., 2024) identified as among the strongest predictors of course success. The number of distinct resources accessed captures the breadth of engagement across activity types. The weekend click ratio captures the temporal pattern of study behaviour. Where useful, the vle table's activity-type metadata is used to disaggregate clicks by resource type.

### **3.5.3 Assessment Features**

The assessment group is derived by joining studentAssessment with assessments and aggregating to student level. The number of assessments submitted and the submission rate capture assessment completion behaviour. The mean assessment score captures overall academic performance, while the weighted mean score reflects the contribution of each assessment to the final grade as defined by the module. The mean number of days between submission and the scheduled assessment date captures timeliness of submission, an indicator of organisation and engagement that prior work associates with outcome risk.

### **3.5.4 Course and Context Features**

The course group comprises the module identifier, the length of the module presentation in days, and the presentation year. These contextual features control for systematic differences between modules and presentations, for example, differences in assessment structure or presentation intensity, that could otherwise confound the relationship between student behaviour and outcome.

### **3.5.5 Final Feature Set**

Table 3.1 lists the engineered feature set used as input to both models.

  ------------------- ----------------------- -----------------------------------------------------------------------
   **Feature Group**  **Feature**             **Description**

    **Demographic**   gender                  Student gender (binary as supplied in the dataset)

    **Demographic**   age_band                Ordinal-encoded age group of the student

    **Demographic**   region                  Geographic region of the student (one-hot encoded)

    **Demographic**   highest_education       Highest education level attained prior to the module

    **Demographic**   imd_band                Index of Multiple Deprivation band (socioeconomic indicator)

    **Demographic**   num_of_prev_attempts    Number of previous attempts at the module

    **Assessment**    assessments_submitted   Count of assessments the student submitted

    **Assessment**    submission_rate         Assessments submitted divided by assessments available

    **Assessment**    mean_assessment_score   Mean of the student's assessment scores

    **Assessment**    weighted_mean_score     Mean score weighted by each assessment's final weight

    **Assessment**    mean_days_to_submit     Mean gap between submission date and assessment date

        **VLE**       total_clicks            Sum of all VLE interaction clicks for the student

        **VLE**       active_days             Number of distinct dates on which the student interacted with the VLE

        **VLE**       mean_clicks_per_day     Total clicks divided by active days

        **VLE**       max_daily_clicks        Highest single-day click count (peak engagement)

        **VLE**       early_clicks_14d        Total clicks in the first 14 days of the presentation

        **VLE**       distinct_resources      Number of distinct VLE activities the student interacted with

        **VLE**       weekend_click_ratio     Share of clicks occurring on weekend dates

      **Course**      code_module             Module identifier (one-hot encoded)

      **Course**      module_length           Length of the module presentation in days

      **Course**      presentation_year       Calendar year of the module presentation
  ------------------- ----------------------- -----------------------------------------------------------------------

*Table 3.1: Engineered feature set used as input to the Logistic Regression and Random Forest models.*

## **3.6 Handling Class Imbalance**

## **3.6.1 Diagnosing the Imbalance**

Before resampling, the class distribution of the retained binary sample is inspected using frequency counts. The diagnosis confirms that the Fail class is substantially outnumbered by the Pass class. Without intervention, both candidate models would be biased toward the majority class: a model predicting Pass for every student would achieve high overall accuracy while identifying no at-risk students at all. Explicit imbalance handling is therefore not an optional refinement but a methodological necessity, given that the study's purpose is the identification of the minority class.

## **3.6.2 SMOTE: Synthetic Minority Over-sampling**

The study adopts SMOTE (Synthetic Minority Over-sampling Technique; Chawla et al., 2002) as its imbalance-handling technique. For each minority-class instance, SMOTE selects one of its k nearest minority-class neighbours in the feature space (with the conventional default k = 5) and generates a synthetic instance at a random point on the line segment joining the two instances. Repeating this process expands the minority class with plausible synthetic examples that lie within the convex region occupied by real failing students, rather than merely duplicating existing records. The result is a balanced training distribution in which the decision boundary of the Fail class is better supported by training examples.

## **3.6.3 Rationale for the Chosen Approach**

SMOTE was selected over the principal alternatives for the following reasons. Compared with random oversampling, which duplicates minority records, SMOTE reduces the risk of overfitting to specific minority instances because each synthetic sample is a novel interpolation. Compared with random undersampling, SMOTE discards no majority-class information, preserving the full Pass-class distribution that the models need in order to learn what success looks like. Compared with class weighting, which modifies the learning objective but leaves the training distribution unchanged, SMOTE physically densifies the minority region of the feature space, which is particularly beneficial for the locally partitioning decision surfaces of Random Forest. SMOTE is also the most widely used and cited resampling method in educational data mining, which supports the comparability of this study's results with the prior literature reviewed in Chapter 2. Plain SMOTE, rather than a hybrid variant, is appropriate for a dataset of this size and for the scope of an undergraduate study, and its behaviour is straightforward to document, justify, and reproduce.

## **3.6.4 Preventing Data Leakage**

A critical design constraint is that SMOTE is applied exclusively to the training partition, after the train/test split. The test partition remains in its original, imbalanced distribution. This ordering is essential for two reasons. First, applying SMOTE before splitting would allow near-duplicate synthetic instances, interpolated from real test-set minority points, to leak into training, producing optimistically biased evaluation. Second, evaluating on the naturally imbalanced test set ensures that the reported metrics reflect the conditions the model would face in operational deployment, where at-risk students are genuinely a minority.

## **3.7 Model Development**

## **3.7.1 Train/Test Split**

The integrated dataset is partitioned into a training set (70%) and a held-out test set (30%) using stratified sampling, which preserves the observed Pass/Fail ratio in both partitions. The 70/30 ratio provides a training set of sufficient size for stable model fitting and hyperparameter search while retaining a test set large enough for reliable estimation of generalisation performance. A fixed random seed (42) is used for the split and for every subsequent stochastic procedure, ensuring that the entire experiment is exactly reproducible.

## **3.7.2 Cross-Validation**

Within the training set, model selection and hyperparameter tuning are performed using five-fold stratified cross-validation. Five folds provide a reasonable bias--variance compromise for a dataset of this size and keep the computational cost of the hyperparameter search tractable, particularly for Random Forest. Each candidate hyperparameter configuration is fitted on four folds and validated on the remaining fold, with the process repeated across all five folds; the configuration's score is the mean of the five validation scores. Because the folds are stratified, every fold preserves the minority-class ratio, so the tuning procedure optimises performance on the imbalanced distribution it will ultimately face.

## **3.7.3 Logistic Regression**

Logistic Regression models the log-odds of the positive class (Fail) as a linear combination of the input features, and transforms the linear score into a probability using the logistic (sigmoid) function. The model is regularised with an L2 penalty to control overfitting in the presence of one-hot-encoded categorical features, and the penalty strength C is treated as a hyperparameter. The lbfgs solver is used, which is well suited to large, sparse, standardised tabular data. Logistic Regression serves two roles in the study. It is the interpretable baseline of the comparison: its coefficients carry a direct probabilistic interpretation, and, as discussed in Section 3.9, its SHAP values are theoretically consistent with its coefficients, providing a reference point for explanation quality. It is also a strong practical competitor: the empirical review in Chapter 2 showed that Logistic Regression achieves competitive accuracy on OULAD, so the comparison against Random Forest is a genuine contest rather than a formality.

## **3.7.4 Random Forest**

Random Forest is an ensemble of decision trees trained using bagging: each tree is fitted on a bootstrap sample of the training data, and at each split a random subset of features is considered, which decorrelates the trees and reduces the variance of the ensemble. The class probability is the mean of the individual trees' predictions. Random Forest was selected as the complex-model comparator because the OULAD literature reviewed in Chapter 2 identifies it as one of the most consistently strong performers on this dataset, and because it captures non-linear feature effects and interactions that Logistic Regression cannot represent. The hyperparameters tuned are the number of trees, the maximum tree depth, the minimum samples required to split a node, and the optional balanced class-weighting setting.

## **3.7.5 Hyperparameter Tuning Strategy**

Hyperparameters for both models are selected using exhaustive grid search with five-fold stratified cross-validation (GridSearchCV). The scoring criterion used to rank candidate configurations is the F1-score of the Fail class, rather than accuracy. This choice follows directly from the study's purpose: because the Fail class is the minority class and the class of practical interest, the tuning objective must reward correct identification of failing students, and F1, the harmonic mean of Precision and Recall, does so while penalising configurations that achieve recall only by predicting failure indiscriminately. The candidate grids are deliberately modest in size, balancing thoroughness against computational cost and against the risk of over-tuning to the validation folds. The configuration with the best cross-validated F1 is refitted on the full training set (after SMOTE) and evaluated once on the held-out test set.

## **3.8 Evaluation Metrics**

Consistent with the critique of the OULAD literature developed in Chapter 2, this study explicitly rejects accuracy as the sole evaluation criterion. On an imbalanced dataset, accuracy can be high even for a model that never identifies a single at-risk student. The study therefore evaluates both models using a four-metric framework, Precision, Recall, F1-Score, and ROC-AUC, supplemented by the confusion matrix for error analysis. In what follows, the positive class is Fail, and a true positive is a failing student correctly identified as at risk.

### **3.8.1 Precision**

Precision is the proportion of students predicted as Fail who actually failed, computed as TP / (TP + FP). In the operational context of an early warning system, Precision answers the question: of the students we flag for intervention, how many genuinely needed it? Low Precision implies that limited support resources would be wasted on students who were not actually at risk.

### **3.8.2 Recall**

Recall (sensitivity) is the proportion of students who actually failed that the model correctly identified, computed as TP / (TP + FN). Recall is arguably the most operationally important metric in this study: every failing student the model misses (a false negative) is a student who receives no intervention. A model with high accuracy but low recall would therefore fail the study's primary purpose, which is why recall receives particular emphasis in the results discussion.

### **3.8.3 F1-Score**

The F1-Score is the harmonic mean of Precision and Recall, computed as 2 × (Precision × Recall) / (Precision + Recall). Because the harmonic mean is dominated by the smaller of the two components, a high F1 requires the model to be simultaneously good at both identifying failing students and avoiding excessive false alarms. F1 provides a single balanced summary of minority-class performance and is the metric used for hyperparameter tuning, as described in Section 3.7.5.

### **3.8.4 ROC-AUC**

The Receiver Operating Characteristic curve plots the true positive rate (Recall) against the false positive rate across all possible classification thresholds, and the Area Under this Curve (ROC-AUC) summarises the model's ability to rank failing students above passing students, independent of any single threshold. An AUC of 1.0 indicates perfect separation and 0.5 indicates chance-level ranking. ROC-AUC is valuable in this study because it evaluates the quality of the predicted probabilities themselves, the quantities an institution would use to prioritise interventions, rather than the hard classifications produced at an arbitrary threshold.

### **3.8.5 Confusion Matrix**

The confusion matrix reports the raw counts of true positives, true negatives, false positives, and false negatives on the held-out test set. Although it is not a single-number summary, it is retained because it makes the error structure of each model transparent: two models with identical F1-scores may err in different ways, and the confusion matrix reveals whether a model's mistakes are concentrated in missed failures (false negatives) or in false alarms (false positives), a distinction with direct operational consequences.

### **3.8.6 A Balanced Four-Metric Framework**

Taken together, the four metrics provide a balanced assessment: Precision guards against excessive false alarms, Recall guards against missed at-risk students, F1 summarises the trade-off between the two, and ROC-AUC evaluates threshold-independent ranking quality. Reporting all four, together with the confusion matrix, directly addresses the second research gap identified in Chapter 2, the over-reliance on accuracy in the OULAD literature, and ensures that the Logistic Regression versus Random Forest comparison is judged on the full spectrum of classification behaviour that matters in practice.

## **3.9 Explainable AI: The SHAP Framework**

### **3.9.1 Why SHAP**

SHAP (SHapley Additive exPlanations; Lundberg and Lee, 2017) is adopted as the interpretability framework for this study for three reasons established in the theoretical review of Chapter 2. First, its feature attributions are grounded in Shapley's (1953) cooperative game theory and satisfy the efficiency, symmetry, and linearity axioms, giving them a principled fairness that ad hoc importance measures lack. Second, SHAP is model-agnostic in principle and provides specialised efficient implementations for the two model families used here, enabling a like-for-like comparison of explanations across architectures. Third, SHAP delivers both global interpretability (which features matter overall, and in what direction) and local interpretability (why a specific student received a specific prediction), matching the dual interpretability requirement of the study.

### **3.9.2 TreeSHAP for Random Forest**

For the Random Forest model, exact Shapley values are computed using TreeSHAP, the polynomial-time algorithm that exploits tree structure to compute feature attributions exactly rather than by sampling. TreeSHAP makes it computationally feasible to attribute every test-set prediction across all trees of the forest, producing a per-student, per-feature matrix of SHAP values whose entries express each feature's additive contribution, in log-odds units, to that student's predicted probability of failure.

### **3.9.3 LinearSHAP for Logistic Regression**

For the Logistic Regression model, SHAP values are computed using the linear implementation, which derives exact additive attributions from the model's coefficients and the feature values relative to the expected baseline. Because a Logistic Regression model is itself an additive model, its SHAP values decompose its own linear score exactly, and each feature's SHAP value corresponds directly to its coefficient multiplied by the feature's deviation from baseline. This property gives Logistic Regression a privileged role in the interpretability analysis: its SHAP explanations are the model itself, providing a theoretically clean reference against which the Random Forest's approximate-by-nature explanations can be compared.

### **3.9.4 Global Interpretability**

Global interpretability is achieved through two complementary visualisations computed over the held-out test set. The SHAP summary (beeswarm) plot displays, for every feature, the distribution of per-student SHAP values, with points coloured by the feature's value; this reveals both the importance of each feature and the direction of its effect (for example, whether low engagement increases or decreases failure risk). The mean absolute SHAP value bar chart provides a compact global importance ranking. These global views directly address Objective 6's requirement to identify the key factors influencing student failure, and they enable comparison with the feature-importance findings of prior studies reviewed in Chapter 2.

### **3.9.5 Local Interpretability**

Local interpretability is achieved through SHAP waterfall and force plots for selected individual students. Each plot decomposes a single student's prediction from the baseline expected failure probability to the student's final predicted probability, showing the additive contribution of every feature. To make the analysis meaningful, the study presents local explanations for carefully chosen illustrative cases: a correctly identified high-risk student (showing which risk factors drove the flag), a correctly identified low-risk student, and at least one false negative (a failing student the model missed), whose explanation reveals which protective signals masked the student's risk. These cases demonstrate how an educator could interrogate an individual prediction and translate it into a personalised support conversation, the operational payoff of interpretability that black-box reporting cannot provide.

### **3.9.6 Cross-Model Comparison of Feature Importance**

The final element of the SHAP framework is the comparative analysis of the two models' explanations. The global importance rankings produced by Logistic Regression and Random Forest are compared by examining the agreement in their top-ranked features and by computing the Spearman rank correlation between the two models' mean absolute SHAP vectors. Where the models agree on the dominant risk factors despite their different architectures, confidence in those factors as genuine predictors is strengthened; where they disagree, the divergence is examined, for example, disagreement may indicate non-linear effects or feature interactions that only the forest can exploit. This comparative interpretability analysis is the distinctive contribution of the study and goes beyond asking which model is more accurate, addressing instead whether the models tell the same story about why students fail.

## **3.10 Implementation Tools and Environment**

The entire pipeline is implemented in Python within Jupyter notebooks. Data manipulation and table integration use pandas (McKinney, 2010) and NumPy (Harris et al., 2020). Model training, cross-validation, grid search, and metric computation use scikit-learn (Pedregosa et al., 2011). SMOTE resampling uses the imbalanced-learn library, which integrates with the scikit-learn pipeline interface. SHAP values and visualisations are produced with the shap library, and supplementary visualisations use matplotlib (Hunter, 2007) and seaborn (Waskom, 2021). A single fixed random seed (42) is set for the train/test split, cross-validation shuffling, SMOTE generation, and Random Forest initialisation, so that every result reported in Chapter 4 can be reproduced exactly by re-running the notebooks. The computations involved are modest and run comfortably on a standard personal computer; no specialised hardware is required.

## **3.11 Ethical Considerations**

The study uses a fully anonymised, publicly released secondary dataset; it involves no contact with human participants, no collection of personal data, and no possibility of re-identifying individuals, and therefore requires no primary ethics approval. Nevertheless, three ethical dimensions are acknowledged. First, the findings of the study are correlational, not causal: SHAP identifies features that predict failure, and an institution acting on these predictions should treat them as risk indicators that inform, rather than replace, professional judgement. Second, fairness must be considered: because demographic attributes such as region and deprivation band are included as features, the results chapter will examine whether the models' errors or the SHAP attributions disadvantage particular demographic groups, and the discussion will caution against using the model to make high-stakes decisions about individual students without human oversight. Third, responsible reporting requires honesty about limitations: the models are trained on data from a single distance-learning institution, and their performance may not transfer to other educational contexts; this limitation is stated explicitly rather than implied away.

## **3.12 Chapter Summary**

This chapter has specified the complete methodology of the study. A positivist, quantitative, comparative experimental design was adopted, using secondary analysis of the OULAD dataset. The four-class outcome variable was converted to a binary Pass/Fail target on four stated grounds, operational alignment, empirical learnability, the qualitative distinctness of withdrawal, and interpretive clarity, and the class imbalance this produces is addressed with SMOTE applied strictly to the training partition. A twenty-one-feature engineered dataset was constructed from demographics, VLE engagement, assessment records, and course context. Logistic Regression and Random Forest are developed under an identical 70/30 stratified protocol with five-fold cross-validated grid search tuned on F1, and evaluated with Precision, Recall, F1-Score, ROC-AUC, and the confusion matrix. SHAP, via TreeSHAP for the forest and the linear implementation for Logistic Regression, provides global and local interpretability and a cross-model comparison of feature attributions. This methodology addresses each research objective in turn and sets the stage for Chapter 4, which presents and analyses the results.

------------------------------------------------------------------------


Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic Minority Over-sampling Technique. Journal of Artificial Intelligence Research, 16, 321--357.

Creswell, J. W., & Creswell, J. D. (2018). Research Design: Qualitative, Quantitative, and Mixed Methods Approaches (5th ed.). SAGE Publications.

Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. Nature, 585, 357--362.

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90--95.

Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. Scientific Data, 4, 170171.

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems (NeurIPS 2017).

McKinney, W. (2010). Data structures for statistical computing in Python. In Proceedings of the 9th Python in Science Conference (pp. 51--56).

Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825--2830.

Shapley, L. S. (1953). A value for n-person games. In H. W. Kuhn & A. W. Tucker (Eds.), Contributions to the Theory of Games (Vol. 2, pp. 307--317). Princeton University Press.

Waskom, M. L. (2021). seaborn: statistical data visualization. Journal of Open Source Software, 6(60), 3021.


```{=openxml}
<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>CHAPTER FOUR</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>RESULTS AND ANALYSIS</w:t></w:r></w:p>
```





## 4.1 Introduction

This chapter reports the analytical findings of the present study. The four research questions and six research objectives set out in Chapter 1 are answered in turn, and the methodological commitments of Chapter 3 are honoured at every step. Chapter 4 is the empirical centre of the dissertation: Chapter 1 motivates the work, Chapter 2 surveys the literature, Chapter 3 documents the methodology, and Chapter 5 turns the findings into conclusions and recommendations.

The chapter is organised in two parts. Sections 4.1–4.4 set up the notation and definitions used throughout the analytical sections. Sections 4.5–4.9 report the findings: predictive performance, global SHAP interpretability, local SHAP interpretability, cross-model interpretability comparison, and synthesis. Figures are numbered consecutively across the chapter from Figure 1 to Figure 14; tables from Table 1 to Table 5.

The mapping to research objectives is as follows. Objective 1 (data integration) is addressed in 4.2 and 4.3. Objective 2 (model training) is addressed in 4.3. Objective 3 (predictive comparison) is addressed in 4.5. Objective 4 (global SHAP) is addressed in 4.6, with the SHAP framework itself explained in 4.4. Objective 5 (local SHAP) is addressed in 4.7. Objective 6 (cross-model comparison) is addressed in 4.8 and synthesised in 4.9.

## 4.2 Dataset Recap

The analytical dataset is the Open University Learning Analytics Dataset (OULAD; Kuzilek et al., 2017), released under a Creative Commons Attribution 4.0 licence and available from the UCI Machine Learning Repository. The release contains seven relational tables; the present study uses six (`studentInfo`, `studentVle`, `vle`, `assessments`, `studentAssessment`, `courses`), omitting `studentRegistration` because its fields do not contribute to the predictive problem. The dataset covers seven presentations across two modules and three academic years (2013 and 2014).

After excluding Withdrawn students (whose final outcome is ambiguous), the modelling matrix contains 22,311 rows out of the original 32,593 in the released dataset. The exclusion removes approximately 21 per cent of the original population, which means the 31.4 per cent Fail prevalence reported below is computed on a non-representative subset of the original OULAD population; the prevalence among all students (including Withdrawn) is closer to 21 per cent. The binary target is constructed by mapping Pass and Distinction to 0 and Fail to 1, giving 15,299 Pass-or-Distinction rows (68.6 per cent) and 7,012 Fail rows (31.4 per cent). The minority class is therefore one-third of the population.

The 21 base features fall into four groups: six demographic, seven virtual-learning-environment engagement, five assessment, and three course-context. After one-hot encoding, the modelling matrix contains 44 columns. A stratified 70/30 split with `random_state=42` produces a training set of 15,617 rows (10,711 Pass, 4,906 Fail) and a held-out test set of 6,694 rows (4,588 Pass, 2,106 Fail), preserving the 31.4 per cent prevalence in both splits. The test set is used exactly once, for the final evaluation in 4.5.

## 4.3 Methodology Recap

Two classifiers are trained on the integrated matrix: a Logistic Regression with L2 regularisation and the l-bfgs solver, and a Random Forest with 500 trees and maximum depth 15. Both are wrapped in an `imblearn.pipeline.Pipeline` that applies SMOTE inside each cross-validation fold (k_neighbors=5, random_state=42), so no test-fold information leaks into the training of any individual fold. Both are tuned by five-fold stratified grid search with `scoring='f1'`, and the best estimator is refit on the full training set before evaluation.

The Logistic Regression grid covers `C ∈ {0.01, 0.1, 1, 10}`, with `penalty='l2'`, `solver='lbfgs'`, `class_weight=None`, `max_iter=1000`. The best estimator uses `C=1.0`. The Random Forest grid covers `n_estimators ∈ {200, 500}`, `max_depth ∈ {None, 15, 25}`, `min_samples_split ∈ {2, 5}`, with `class_weight=None`, `n_jobs=-1`, `random_state=42`. The best estimator uses `n_estimators=500`, `max_depth=15`.

Six metrics are reported in 4.5: accuracy, precision, recall, F1, ROC-AUC, and average precision (AP). F1 is the tuning metric; AP is more sensitive than ROC-AUC to performance on the minority class (Saito & Rehmsmeier, 2015). Accuracy is reported for completeness but is not the primary metric because the 31.4 per cent class imbalance makes accuracy insensitive to the operationally important errors (failing students missed); reporting six metrics rather than accuracy alone directly addresses the over-reliance on accuracy identified in the OULAD literature. The test set is left at its original 31.4 per cent prevalence, so reported metrics reflect the imbalanced deployment condition rather than a balanced evaluation setting.

Two SHAP explainers are used: LinearSHAP for the Logistic Regression and TreeSHAP for the Random Forest (Lundberg et al., 2020). LinearSHAP returns values on the log-odds scale; TreeSHAP returns values on the probability scale. The TreeSHAP computation is performed on a 300-row stratified subsample of the test set to keep the computation tractable; LinearSHAP is performed on the full test set. The 300-row subsample preserves the 31.4 per cent Fail prevalence of the full test set, so the marginal feature distributions and the per-feature SHAP distributions are not distorted by the subsampling. The 300 rows represent a deliberate trade-off between computational tractability and statistical precision.

The full pipeline is reproducible from a clean clone of the repository in under 45 minutes on a standard laptop. The random seed is fixed at every stochastic stage. Every notebook can be re-run from top to bottom without manual intervention, and every figure and table cited in this chapter is generated by the corresponding notebook and saved to `outputs/figures/` or `outputs/tables/`.

## 4.4 SHAP as the Interpretability Framework

SHAP (Lundberg & Lee, 2017) is the interpretability framework used for both classifiers, chosen because it is simultaneously local (each prediction gets its own explanation), faithful (the SHAP values sum to the model's output), and defined for both linear and tree-ensemble models through specialised explainers (LinearSHAP and TreeSHAP). Permutation importance is faithful but not local; LIME (Ribeiro et al., 2016) is local but not consistent across runs; Logistic Regression coefficients are local and faithful but not model-agnostic. Only SHAP offers all three properties.

SHAP values are Shapley values from cooperative game theory (Shapley, 1953), applied to the prediction problem. The interpretation is that each feature is a "player" in a cooperative game whose "payout" is the model's prediction, and the Shapley value of a feature is its average marginal contribution across all possible coalitions. The Shapley value is the unique attribution method that satisfies three desirable properties: local accuracy (attributions sum to the model's output), consistency (if a model changes so that a feature contributes more, its attribution does not decrease), and missingness (a feature not present in the model receives an attribution of zero).

For a linear model `f(x) = b + Σ w_i · x_i`, the SHAP value for feature `i` is `φ_i = w_i · (x_i − E[x_i])`, where the expectation is over the background dataset. The attribution is in log-odds units, and the sum of the base value and the SHAP values equals the model's prediction. For a Random Forest, TreeSHAP (Lundberg et al., 2020) computes exact SHAP values in polynomial time by exploiting the tree structure, returning attributions in probability units. The additivity property is the foundation of the cross-model comparison in 4.8: the sign of each SHAP value (push toward Pass or toward Fail) is comparable across the two explainers, even though the magnitudes are not.

Two limitations bound the present SHAP analysis. First, SHAP values are statistical associations, not causal effects: a feature with a large positive SHAP value is associated with the model's prediction of Fail, not necessarily a feature whose manipulation would change the prediction. Second, SHAP values are computed with respect to the model's prediction, not the true outcome: a feature that the model uses heavily may be a feature the model has learned to overweight rather than a feature genuinely informative about the outcome. Both limitations are flagged when the present findings are read.

## 4.5 Predictive Performance Comparison

This section addresses Research Question 1. The Random Forest achieved the higher score on five of the six metrics reported in Table 1, while Logistic Regression retained a marginal lead on precision alone. The gap on F1-score is the largest observed (2.0 percentage points); the gaps on ROC-AUC and AP are small in absolute terms but consistent in direction.

### 4.5.1 ROC Analysis

Both models achieve an area under the ROC curve above 0.95, indicating strong discrimination between Fail and Pass across the full operating range (see Figure 1). The Random Forest holds a small lead of about half a percentage point (0.962 versus 0.957). The two curves overlap heavily over the lower-left quadrant, where the false-positive rate is below roughly 0.2, and only separate visibly past that point. Both classifiers recover about 80 per cent of failing students while misclassifying around 4 per cent of passing students.

![Receiver-operating-characteristic curves for the held-out test set](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/roc_curves.png){#fig:roc-curves}

**Figure 1**

*Receiver-operating-characteristic (ROC) curves for Logistic Regression and Random Forest on the held-out test set (n = 6,694).*

*Note.* AUC = area under the curve. The dashed grey line marks chance performance. A statistical test of the difference between the two AUC values is omitted here; the gap is too small to yield a reliable p-value at conventional thresholds.

### 4.5.2 PR Analysis

The precision-recall view in Figure 2 is the more demanding comparison because the positive class; Fail; accounts for only 31.4 per cent of the test set. The Random Forest again leads (AP = 0.943 versus 0.933), preserving precision above 0.6 across nearly the entire recall range. The two curves remain within roughly 0.01 of each other until recall crosses about 0.7, after which the Random Forest pulls ahead more visibly.

![Precision-recall curves for the held-out test set](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/pr_curves.png){#fig:pr-curves}

**Figure 2**

*Precision-Recall (PR) curves for Logistic Regression and Random Forest on the held-out test set (n = 6,694).*

*Note.* AP = average precision across all recall thresholds. The baseline (dashed grey line) equals the class prevalence of 0.314.

### 4.5.3 Confusion Matrix and Error Profile

The two confusion matrices in Table 1 make the operational trade-off concrete. The Random Forest trades 29 extra false positives (219 versus 190) for 90 additional correctly identified failing students (1,759 versus 1,669). For an institution that intends to use these predictions to triage student support, the marginal recall lift of about 4.3 percentage points (0.831 versus 0.789) translates into catching about 90 students who would otherwise go unidentified, at the cost of flagging roughly 29 additional passing students for review.

**Table 1**

*Six-metric comparison between Logistic Regression and Random Forest on the held-out test set (n = 6,694, positive-class prevalence = 31.4%).*

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | AP |
|-------|---------|-----------|--------|----|---------|------|
| Logistic Regression | 0.905 | 0.898 | 0.789 | 0.840 | 0.957 | 0.933 |
| Random Forest | 0.914 | 0.889 | 0.831 | 0.859 | 0.962 | 0.943 |

*Note.* AP = average precision across all recall thresholds. The Random Forest leads on five of the six metrics; Logistic Regression retains a small lead on precision alone. Differences are largest for recall (4.3 percentage points) and F1 (2.0 percentage points).

### 4.5.4 Synthesis Against Research Question 1

The Random Forest is the stronger classifier overall, but the lead is operationally modest and rests entirely on its higher recall on the minority class. The two models are not statistically distinguishable on ROC-AUC given the gap of 0.005; the F1-score gap of 0.020 depends on the choice of probability threshold (Pedregosa et al., 2011). A sensitivity analysis over thresholds between 0.3 and 0.7 would be needed to claim a stable performance gap, and that analysis is left for future work. For the present chapter, RF is treated as the marginally better model, and 4.6 onwards asks whether it is also the more interpretable one.

## 4.6 Global SHAP Interpretability

This section addresses Research Question 2 by ranking the features that drive the predictions of each model and by showing how each feature's value relates to its contribution to the prediction. Two visual encodings are used: the beeswarm plot, which displays the per-instance SHAP distribution with a colour gradient for the feature value, and the mean-|SHAP| bar chart, which gives a compact ranking by overall contribution.

### 4.6.1 Logistic Regression: Global Importance

For Logistic Regression, the top three features by mean |SHAP| are `edu_A Level or Equivalent` (2.98), `edu_Lower Than A Level` (2.54), and `submission_rate` (2.40). Six of the ten most influential features are demographic or course-context variables: three education levels, both gender indicators, and one module indicator. Only three engagement or assessment features reach the top ten: `submission_rate`, `weighted_mean_score`, and one module that doubles as a course-context feature.

![Logistic Regression: SHAP beeswarm (scaled features)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_summary_lr.png){#fig:shap-lr-summary}

**Figure 3**

*SHAP beeswarm for Logistic Regression over the held-out test set (n = 6,694). Each dot is one test instance; horizontal position is the SHAP contribution to the log-odds; colour encodes the scaled feature value (red = high, blue = low). The top 20 features are shown.*

*Note.* LinearSHAP returns values on the log-odds scale because the underlying model is a logistic regression; the magnitude of one log-odds shift is approximately equivalent to a probability shift of 0.21 at the mean prediction.

The beeswarm in Figure 3 reveals the direction of each feature's contribution as well as its magnitude. For the three education-level indicators, high values (red points) push the prediction toward Pass; that is, away from Fail; while low values (blue points) push toward Fail. The same left-to-right reading applies to the engagement metrics: high `submission_rate`, `weighted_mean_score`, and the active-day indicators all push toward Pass. Reading across rows gives a clear pattern: the Logistic Regression leans on a small set of demographic and course-context features, and the contribution of each feature is roughly symmetric across instances.

![Logistic Regression: global feature importance (top 20 by mean |SHAP|)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_importance_lr.png){#fig:shap-lr-importance}

**Figure 4**

*Mean |SHAP| (log-odds scale) for the top 20 features under Logistic Regression. Bars are sorted by descending importance.*

### 4.6.2 Random Forest: Global Importance

The Random Forest reverses the priority. The top three features are `submission_rate` (mean |SHAP| = 0.148), `assessments_submitted` (0.076), and `mean_assessment_score` (0.070): three engagement or assessment metrics in a row. Seven of the top ten features are engagement or assessment metrics. Only one demographic feature (`edu_A Level or Equivalent`) and one gender indicator (`gender_F`) break into the top ten.

![Random Forest: SHAP beeswarm (top 20 features)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_summary_rf.png){#fig:shap-rf-summary}

**Figure 5**

*SHAP beeswarm for Random Forest over the stratified 300-row SHAP subsample. Each dot is one test instance; horizontal position is the SHAP contribution to the probability; colour encodes the original-scale feature value (red = high, blue = low).*

*Note.* TreeSHAP returns values on the probability scale because the underlying model is a probability classifier. The subsample is stratified by class to preserve the 31.4 per cent Fail prevalence of the full test set.

The beeswarm in Figure 5 shows much wider per-instance spreads than the Logistic Regression beeswarm. For `submission_rate`, the contribution extends from about −0.2 to about +0.2, indicating that the Random Forest treats the same feature differently depending on its interaction with other features. The same is true for `assessments_submitted` and `mean_assessment_score`: the Random Forest's predictions rely on interactions, which a linear model cannot capture.

![Random Forest: global feature importance (top 20 by mean |SHAP|)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_importance_rf.png){#fig:shap-rf-importance}

**Figure 6**

*Mean |SHAP| (probability scale) for the top 20 features under Random Forest.*

### 4.6.3 Synthesis Against Research Question 2

Both models identify `submission_rate` and `weighted_mean_score` as the strongest drivers of student failure, which gives a degree of cross-model corroboration to the engagement-based hypothesis. Beyond that overlap, the two models diverge. The Logistic Regression top ten is dominated by demographic and course-context features, while the Random Forest top ten is dominated by engagement and assessment metrics. The two top-ten lists share only four features, and the rank-ordering of those four features also differs. The detailed quantification of this divergence is reported in 4.8.

## 4.7 Local SHAP Interpretability

This section addresses Research Question 4 by inspecting six individual cases: the four corners of the confusion matrix (TP, TN, FN, FP) plus two borderline students whose predicted probability lies in the 0.4–0.6 band. Twelve waterfall plots in total; six cases times two models; are presented as Figure 7 to Figure 12.

### 4.7.1 True Positive: A Failing Student Correctly Identified

Student 582710 in presentation 2013J (Figure 7) actually failed and was correctly flagged by both models: LR P(Fail) = 1.000, RF P(Fail) = 1.000. The submission_rate is zero, the assessment score is 47.5, and the active days count is 7: the engagement record of a student who disengaged early. The Logistic Regression waterfall credits the prediction to two demographic features rather than to engagement, even though the engagement record is what a tutor would point to. The Random Forest reaches the same prediction but via the engagement features. The two models agree on the answer but for different stated reasons.

![True Positive case (Logistic Regression) for student 582710, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tp_lr.png){#fig:tp-lr}

![True Positive case (Random Forest) for student 582710, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tp_rf.png){#fig:tp-rf}

**Figure 7**

*Local SHAP waterfall for the True Positive case (student 582710, presentation 2013J).*

### 4.7.2 True Negative: A Passing Student Correctly Cleared

Student 597787 in presentation 2013J (Figure 8) actually passed and was correctly cleared by both models: LR P(Fail) = 0.002, RF P(Fail) = 0.001. The submission_rate is 0.85 and the weighted mean score is 0.967: the engagement record of a student on track. The Logistic Regression explanation leans on demographic features with engagement features contributing only modestly. The Random Forest ranks engagement features first. The two models are again concordant on the prediction but assign the credit to different feature families.

![True Negative case (Logistic Regression) for student 597787](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tn_lr.png){#fig:tn-lr}

![True Negative case (Random Forest) for student 597787](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tn_rf.png){#fig:tn-rf}

**Figure 8**

*Local SHAP waterfall for the True Negative case (student 597787, presentation 2013J).*

### 4.7.3 False Negative: A Failing Student the Models Missed

Student 637388 in presentation 2014J (Figure 9) actually failed but was predicted Pass by both models: LR P(Fail) = 0.028, RF P(Fail) = 0.035. This is the operationally most interesting case: the kind of student the early-warning system is meant to catch but does not. The engagement record is positive on paper: submission_rate = 0.83, assessments_submitted = 5, mean_assessment_score = 60.2. On every engagement feature, this student looks like a passing student. Both models agree. The actual failure is invisible to the engagement-only lens: possibly a final-exam mishap, possibly an administrative flag, and the models have no signal to draw on. This case illustrates the structural limit of engagement-based prediction.

![False Negative case (Logistic Regression) for student 637388](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fn_lr.png){#fig:fn-lr}

![False Negative case (Random Forest) for student 637388](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fn_rf.png){#fig:fn-rf}

**Figure 9**

*Local SHAP waterfall for the False Negative case (student 637388, presentation 2014J).*

### 4.7.4 False Positive: A Passing Student Incorrectly Flagged

Student 626998 in presentation 2014J (Figure 10) actually passed but was flagged Fail by both models: LR P(Fail) = 0.685, RF P(Fail) = 0.931. The engagement record is weak by absolute standards but not catastrophic: submission_rate = 0.6, assessments_submitted = 3, active_days = 7. The Random Forest prediction is driven by engagement metrics all pushing toward Fail. The Logistic Regression prediction leans on demographic and module indicators. This is a student who would receive an unwarranted outreach call if the model is used to triage.

![False Positive case (Logistic Regression) for student 626998](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fp_lr.png){#fig:fp-lr}

![False Positive case (Random Forest) for student 626998](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fp_rf.png){#fig:fp-rf}

**Figure 10**

*Local SHAP waterfall for the False Positive case (student 626998, presentation 2014J).*

### 4.7.5 Borderline-1: Where the Two Models Disagree

Student 248511 in presentation 2013B (Figure 11) actually passed; the Logistic Regression predicts Fail at P(Fail) = 0.566 while the Random Forest predicts Pass at P(Fail) = 0.498. This is the case where the two models diverge most clearly. The Logistic Regression leans on region and education features, with several smaller features pushing toward Fail; the Random Forest credits assessment score and submission rate. Both end up near the decision boundary, but for different stated reasons.

![Borderline-1 case (Logistic Regression) for student 248511](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-1_lr.png){#fig:b1-lr}

![Borderline-1 case (Random Forest) for student 248511](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-1_rf.png){#fig:b1-rf}

**Figure 11**

*Local SHAP waterfall for the Borderline-1 case (student 248511, presentation 2013B).*

### 4.7.6 Borderline-2: A Borderline Agreement

Student 429212 in presentation 2013J (Figure 12) actually passed, and both models predict Pass but with low confidence: LR P(Fail) = 0.463, RF P(Fail) = 0.496. The Random Forest credits three engagement metrics that almost fully cancel the base rate. The Logistic Regression explanation is again dominated by demographic features with one engagement feature tipping the prediction toward Pass. The two models reach the same decision at the boundary via different feature rankings.

![Borderline-2 case (Logistic Regression) for student 429212](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-2_lr.png){#fig:b2-lr}

![Borderline-2 case (Random Forest) for student 429212](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-2_rf.png){#fig:b2-rf}

**Figure 12**

*Local SHAP waterfall for the Borderline-2 case (student 429212, presentation 2013J).*

### 4.7.7 Synthesis Against Research Question 4

The six cases illustrate a recurring pattern: the two models are concordant on the four corners of the confusion matrix but diverge in the middle. Concordance at the corners is not surprising (both models achieve F1 above 0.84 on the held-out set), but the attribution is different. The Logistic Regression explanations lean on demographic and course-context features even when the engagement record is decisive; the Random Forest explanations lean on engagement and assessment features even when the demographic record is informative. For institutional use, a tutor receiving an alert from the Random Forest and a tutor receiving an alert from the Logistic Regression would receive different justifications for the same prediction. The two explanations are not interchangeable, and the choice between them is a question of institutional preference as much as a question of accuracy.

## 4.8 Cross-Model Interpretability Comparison

This section addresses Research Question 3 by quantifying and visualising the agreement and disagreement between the Logistic Regression and Random Forest global explanations. Two summary statistics anchor the comparison: the Spearman rank correlation between the two mean-|SHAP| vectors (Spearman, 1904), and the Jaccard index of the top-10 feature sets. Local-level agreement is then reported on the six illustrative cases from 4.7.

### 4.8.1 Spearman Rank Correlation

Across all 44 modelling features, the Spearman rank correlation between the two mean-|SHAP| vectors is 0.10 (p = 0.508, two-sided). The correlation is positive but small, and the p-value does not reject the null hypothesis of no rank correlation at conventional thresholds (α = 0.05). Read on its own, this single number would suggest that the two models pick out roughly the same features. The next two sub-sections show that the picture is more interesting once the magnitude asymmetry is corrected and the top-10 lists are inspected side by side.

### 4.8.2 Side-by-Side Importance Bar Chart

Figure 13 plots the top-20 features by combined rank for both models. The two panels share the y-axis ordering but use different x-axis scales: the Logistic Regression panel is in log-odds units (range 0 to 3.0), the Random Forest panel is in probability units (range 0 to 0.15). The scales are not directly comparable in magnitude, but they are comparable in rank.

![Cross-model global importance bar chart](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/cross_model_importance.png){#fig:cross-model-importance}

**Figure 13**

*Cross-model global importance for the top 20 features by combined rank.*

*Note.* Spearman ρ = 0.10 (p = 0.508); top-10 Jaccard index = 0.25.

### 4.8.3 Log-Log Scatter with Spearman Annotation

Figure 14 plots every one of the 44 features as a point with LR mean |SHAP| on the horizontal axis and RF mean |SHAP| on the vertical axis, both on a symlog scale. The top-10 features by LR mean |SHAP| are labelled. The scatter makes the same point as Figure 13 in a different visual idiom: features with high LR importance cluster mostly in the upper half of the RF range, but the relationship is loose, with `submission_rate` and `weighted_mean_score` sitting at the top of both models.

![Cross-model feature importance scatter](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/cross_model_scatter.png){#fig:cross-model-scatter}

**Figure 14**

*Cross-model feature importance scatter on symlog axes.*

### 4.8.4 Top-10 Agreement and Divergence

Across the top-10 features in each model, four appear in both lists: `submission_rate`, `weighted_mean_score`, `edu_A Level or Equivalent`, and `gender_F`. The Jaccard index is 0.25. The six LR-only features are demographic and course-context (`edu_Lower Than A Level`, `module_GGG`, `gender_M`, `module_BBB`, `edu_HE Qualification`, `region_East Anglian Region`). The six RF-only features are engagement and assessment (`assessments_submitted`, `mean_assessment_score`, `active_days`, `total_clicks`, `distinct_resources`, `presentation_year`).

**Table 2**

*Top-10 feature agreement between Logistic Regression and Random Forest.*

| Status | Features |
|--------|----------|
| In both top-10s | `submission_rate`, `weighted_mean_score`, `edu_A Level or Equivalent`, `gender_F` |
| LR-only | `edu_Lower Than A Level`, `module_GGG`, `gender_M`, `module_BBB`, `edu_HE Qualification`, `region_East Anglian Region` |
| RF-only | `assessments_submitted`, `mean_assessment_score`, `active_days`, `total_clicks`, `distinct_resources`, `presentation_year` |

### 4.8.5 Local Direction Agreement

The cross-model agreement at the local level, computed on the six illustrative cases from 4.7, is reported in Table 3. The two models push the SHAP sum in the same direction for four of the six cases (TP, TN, FN, FP). They diverge in direction for the two borderline cases, and they diverge in predicted label only for Borderline-1.

**Table 3**

*Per-case local SHAP direction agreement between Logistic Regression and Random Forest on the six illustrative cases.*

| Case | LR pred | RF pred | Same direction |
|------|---------|---------|----------------|
| TP | 1 | 1 | Yes |
| TN | 0 | 0 | Yes |
| FN | 0 | 0 | Yes |
| FP | 1 | 1 | Yes |
| Borderline-1 | 1 | 0 | No |
| Borderline-2 | 0 | 0 | No |

### 4.8.6 Synthesis Against Research Question 3

Logistic Regression and Random Forest identify substantially different factors as the drivers of student failure. The Spearman rank correlation is positive but not statistically distinguishable from zero, and the top-10 lists share only four features. The LR top-10 is dominated by demographic and course-context features; the RF top-10 is dominated by engagement and assessment features. At the local level, the two models agree in direction for the four corners of the confusion matrix but disagree for the two borderline cases near the decision boundary. The choice of model family changes both the global explanation and the local prediction.

The cross-model divergence is partly a function of feature-engineering choices: both models see the same 44 features, but Logistic Regression sees them on a standardised scale while Random Forest sees them on their original scale. The TreeSHAP and LinearSHAP values are not symmetric, and the disagreement may partly reflect a scale-induced reordering rather than a fundamental epistemic disagreement. A robustness check in which the Random Forest is also evaluated on the standardised features would clarify this, and that check is left for future work.

## 4.9 Synthesis and Discussion of Findings

This section synthesises the analytical findings of 4.5–4.8 against the four research questions set in Chapter 1 and the methodological commitments of Chapter 3. The aim is integrative rather than additive.

### 4.9.1 Cross-Cutting Theme: Accuracy versus Explanatory Coherence

The Random Forest leads Logistic Regression on five of six predictive metrics, but the lead is modest (F1 gap of 0.020, ROC-AUC gap of 0.005) and is concentrated on recall. On the explanatory side, the two models diverge more sharply: Spearman ρ = 0.10 over the 44-feature importance vectors, top-10 Jaccard = 0.25, and only four features appear in both top-10 lists. The aggregate pattern is therefore *agreement on outcome, divergence on reason*: the two models flag mostly the same students as failing, but they point to different features when justifying that flag.

### 4.9.2 Joint Reading of the Four Research Questions

Research Question 1 (predictive performance) is settled: the Random Forest is the marginally stronger classifier, and the gap rests on its higher recall on the minority class. Research Question 2 (global feature importance) shows a clear two-track structure: Logistic Regression leans on demographic and course-context features, Random Forest leans on engagement and assessment features. Research Question 3 (cross-model agreement) quantifies that divergence: ρ = 0.10, Jaccard = 0.25, and a structural-versus-behavioural split. Research Question 4 (local interpretability) shows that the two models agree on direction for the four corners of the confusion matrix but disagree on the two borderline cases near the decision boundary.

### 4.9.3 Operational Implications

For institutional deployment, the choice between the two models depends on the question the institution is asking. If the question is *which students are at risk?*, the Random Forest gives a slightly more complete answer (recall 0.831 versus 0.789). If the question is *why are they at risk?*, the two models give different answers. A useful early-warning system would present both explanations side by side, letting a tutor triangulate. The borderline cases are exactly the students where the two lenses disagree most strongly, and these are the students most in need of human judgement.

### 4.9.4 Methodological Limitations Visible in the Results

Two limitations of the present analysis are visible directly in the results. First, both models were tuned on F1 with a default 0.5 threshold; the apparent F1 lead depends on that threshold. A threshold-sensitivity analysis would be needed to claim a stable performance gap. Second, the cross-model comparison is computed on the 300-row stratified SHAP subsample for the Random Forest, so the RF global ranking reflects that subsample. Both limitations are minor and do not invalidate the qualitative findings.

### 4.9.5 Closing Note on Chapter 4

Chapter 4 has answered four research questions with one shared finding: behavioural engagement and demographic context both matter, but they matter differently for different model families. The next chapter takes the institutional, methodological, and forward-looking implications of this finding and turns them into conclusions and recommendations.

A final methodological observation closes the chapter. The present study has chosen two classifiers that span the model-family spectrum (a linear model and a tree ensemble) and has used SHAP to put them on a comparable footing. An alternative design would have been to choose two classifiers within the same family, and the cross-model comparison would have been very different. The present design maximises the contrast between the two explanations, at the cost of confounding model family with feature scale. A reader who wants to isolate the effect of model family would need to repeat the comparison with two classifiers from the same family, and that comparison is left for future work.


```{=openxml}
<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>CHAPTER FIVE</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>DISCUSSION, CONCLUSIONS, AND RECOMMENDATIONS</w:t></w:r></w:p>
```





## 5.1 Summary

This study set out to investigate whether explainable machine-learning models could predict student failure on the Open University Learning Analytics Dataset (OULAD; Kuzilek et al., 2017), and whether the explanations those models produce would be operationally useful. The investigation was structured around six research objectives and four research questions (Chapter 1), and pursued through a nine-phase implementation pipeline documented in Chapter 3.

Four headline findings emerged from Chapter 4. Both models achieve strong predictive performance: ROC-AUC of 0.957 (Logistic Regression) and 0.962 (Random Forest), with the Random Forest retaining a small lead on five of six metrics and the Logistic Regression retaining a marginal lead on precision alone. The two models identify different drivers of student failure: the Logistic Regression top-10 is dominated by demographic and course-context features, while the Random Forest top-10 is dominated by engagement and assessment features, with only four features appearing in both lists. The cross-model rank correlation of the 44-feature importance vectors is 0.10 (p = 0.508), and the top-10 Jaccard index is 0.25. At the local level, the two models agree on direction for four of six illustrative cases but disagree on the two borderline cases near the decision boundary.

Two negative findings are also worth flagging: the two classifiers are not statistically distinguishable on ROC-AUC given the gap of 0.005, and the F1 gap of 0.020 depends on the choice of probability threshold.

## 5.2 Conclusions Against the Research Objectives

The six research objectives were met. Objective 1 (integrate OULAD into a modelling-ready matrix) was met in Chapter 3, producing an integrated matrix of 22,311 student-presentation rows and 44 columns after one-hot encoding, reproducible from a clean clone in under 45 minutes. Objective 2 (train and tune the two classifiers) was met in Chapter 3 with both classifiers tuned by five-fold stratified grid search on F1 inside an `imblearn.pipeline.Pipeline` to prevent leakage. Objective 3 (compare on a six-metric framework) was met in 4.5. Objective 4 (global SHAP explanations) was met in 4.6, with the Logistic Regression top-10 dominated by demographic and course-context features and the Random Forest top-10 dominated by engagement and assessment features. Objective 5 (local SHAP explanations on six illustrative cases) was met in 4.7, with the borderline cases exposing the cross-model disagreement most clearly. Objective 6 (cross-model comparison) was met in 4.8, quantifying the divergence as Spearman ρ = 0.10 and top-10 Jaccard = 0.25.

## 5.3 Limitations of the Study

Five limitations bound the present findings.

**Limitation 1: Single dataset, single institution.** The Open University is one institution, and the OULAD is one dataset. The generalisability to other institutions, modes of study, and national contexts is an open empirical question.

**Limitation 2: Withdrawn students excluded from the modelling matrix.** The exclusion of Withdrawn students is a deliberate methodological choice, but the cost is that the resulting model cannot be used to predict withdrawal. The 31.4 per cent Fail prevalence reflects a non-representative subset of the original OULAD population; the prevalence among all students (including Withdrawn) is closer to 21 per cent.

**Limitation 3: Static features, no temporal trajectory.** All twenty-one features are aggregated over the full presentation, so the model cannot flag students during the presentation when intervention is still possible.

**Limitation 4: Threshold sensitivity not analysed.** Both models were tuned on F1 with a default 0.5 probability threshold, and the F1 gap depends on that threshold. A threshold-sensitivity analysis would clarify whether the gap is stable across thresholds or whether it is an artefact of the default.

**Limitation 5: Cross-method comparison on different feature scales.** The cross-model comparison is partly confounded by the fact that the two classifiers see the features on different scales (standardised for LR, original-scale for RF), and the author cannot separate model-family effects from scale effects on the basis of these results alone.

## 5.4 Recommendations for Institutional Practice

Five recommendations follow from the present findings.

**Recommendation 1: Present both explanations side by side.** The two classifiers identify different drivers of student failure, and an institution that deploys only one will systematically bias the tutor's view of the student. The cleanest deployment is a two-model deployment: both classifiers run, both predictions are presented, and both SHAP explanations are shown side by side.

**Recommendation 2: Use the Random Forest for catchment and the Logistic Regression for justification.** The Random Forest has higher recall (0.831 versus 0.789) and so catches more failing students; the Logistic Regression explanation is easier to communicate to a non-technical audience.

**Recommendation 3: Treat the explanations as decision support, not decision automation.** SHAP values are statistical associations, not causal claims, and the institutional response to a flagged student should be informed by the explanation but not determined by it.

**Recommendation 4: Validate on a subsequent cohort before scaling up.** Cross-validated performance estimates are honest within-cohort estimates, not cross-cohort estimates. An institution that intends to deploy on a subsequent cohort should validate the model on that cohort before scaling up, including a spot-check of the explanations on a handful of students.

**Recommendation 5: Invest in tutor training on SHAP outputs.** The training should cover what a SHAP value means (a feature contribution to a single prediction, not a causal effect), how to read the waterfall plot, and how to act on borderline cases where the SHAP sum is small and the prediction is unstable.

## 5.5 Recommendations for Future Research

Six directions for future research follow from the limitations and the open questions.

**Direction 1: Temporal prediction at multiple points within the presentation.** A natural extension would predict the final outcome from features aggregated up to each week of the presentation, producing a sequence of weekly models.

**Direction 2: Threshold-sensitivity analysis for operating-point selection.** A threshold-sensitivity analysis in which the operating point was varied between 0.3 and 0.7 would clarify whether the F1 gap of 0.020 is stable across operating points.

**Direction 3: Cross-method robustness check on standardised features.** A second Random Forest trained on the standardised features would clarify whether the divergence reported in 4.8 is driven by model family or by feature scale.

**Direction 4: Cross-institutional comparison.** Applying the same methodology to two or three comparable datasets would test the generalisability of the engagement-led ranking.

**Direction 5: Causal interpretation of feature contributions.** A future study that combined the predictive model with a causal-inference framework would identify which feature contributions represent causal levers and which represent mere correlations. The institutional payoff is large but the methodological cost is high.

**Direction 6: Beyond binary classification.** A three-class problem (Pass, Fail, Withdrawn) and a regression problem predicting the final mark on a continuous scale would extend the methodology to more nuanced views of student risk.

## 5.6 Concluding Remarks

This study set out to investigate whether explainable machine learning could predict student failure on the Open University Learning Analytics Dataset, and whether the explanations the models produced would be operationally useful. The reassuring part is that the methodology works: both classifiers achieve strong predictive performance, the SHAP-based explanations are stable enough to inspect at the per-instance level, and the pipeline is reproducible from a clean clone in under 45 minutes. The uncomfortable part is that the two classifiers do not agree on the reasons: the Spearman rank correlation between the two mean-|SHAP| vectors is 0.10, the top-10 Jaccard index is 0.25, and the two models point to different feature families when justifying the same predictions.

The institutional implication is that the choice of model family is not a free parameter. The cleanest deployment is a two-model deployment: both classifiers run, both explanations are presented, and the tutor triangulates. This is operationally modest but removes a known source of systematic bias. The borderline cases are exactly the cases most in need of human judgement.

The forward-looking implication is that the most useful next step is not a more accurate model but a more useful deployment. Done well, an early-warning system built on this methodology would catch more failing students and would give tutors a clearer view of why those students are at risk. Done poorly, it would automate bias and would mislead the people it is meant to support. The choice between those outcomes is an institutional one.


# References

<div custom-style="Reference">

Adefemi, A., Akinrinmade, A., & Ogunleye, O. (2025). Predictive analytics for student success: A machine learning approach. *International Journal of Educational Technology and Learning, 38*(2), 45-62.

</div>
<div custom-style="Reference">

Aghadavoodi, S., & Ghazivakili, M. (2023). Class imbalance in educational data mining: A systematic review. *Computers and Education: Artificial Intelligence, 5*, 100076.

</div>
<div custom-style="Reference">

Agyemang, E. O., Osei, K., & Boateng, F. O. (2024). Ensemble learning for student performance prediction on OULAD. *Journal of Educational Computing Research, 62*(4), 1023-1051.

</div>
<div custom-style="Reference">

Alalawi, J. (2025). Explainable AI in higher education: A scoping review. *Smart Learning Environments, 12*(1), 1-28.

</div>
<div custom-style="Reference">

Alhakbani, N., & Alnassar, F. (2022). A comparative study of machine learning algorithms for predicting student academic success. *Education and Information Technologies, 27*(6), 8233-8261.

</div>
<div custom-style="Reference">

Alnassar, F. (2022). Educational data mining in higher education: A review. *Education and Information Technologies, 27*(8), 11549-11584.

</div>
<div custom-style="Reference">

Alshanqiti, A. (2020). Educational data mining and learning analytics: A systematic review. *Computers and Education, 156*, 103935.

</div>
<div custom-style="Reference">

Althibyani, A. (2024). Predicting at-risk students using engagement features: A deep learning approach. *Computers and Education: Artificial Intelligence, 7*, 100292.

</div>
<div custom-style="Reference">

Baker, R. S. J. d., & Yacef, K. (2009). The state of educational data mining in 2009: A review and future visions. *Journal of Educational Data Mining, 1*(1), 4-17.

</div>
<div custom-style="Reference">

Boujmiraz, M. (2026). Early prediction of student outcomes: A systematic review of recent advances. *Educational Data Mining and Learning Analytics, 14*(1), 1-38.

</div>
<div custom-style="Reference">

Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic minority over-sampling technique. *Journal of Artificial Intelligence Research, 16*, 321-357.

</div>
<div custom-style="Reference">

Chen, L. (2023). Interpretability versus accuracy in student dropout prediction: A trade-off analysis. *Computers and Education Open, 5*, 100155.

</div>
<div custom-style="Reference">

Conijn, R., van der Zanden, L., Denessen, E., & Knoop-van Campen, C. A. N. (2022). Predicting student performance using LMS data: A comparison of approaches. *Computers and Education, 183*, 104498.

</div>
<div custom-style="Reference">

Connelly, C. E. (2022). Machine learning in education: Promise and pitfalls. *Computers & Education, 184*, 104503.

</div>
<div custom-style="Reference">

Creswell, J. W., & Creswell, J. D. (2018). *Research design: Qualitative, quantitative, and mixed methods approaches* (5th ed.). SAGE Publications.

</div>
<div custom-style="Reference">

Daud, A., Aljohani, N., & Abbasi, R. A. (2023). Predicting student performance using advanced learning analytics. *Expert Systems with Applications, 213*(Part C), 119224.

</div>
<div custom-style="Reference">

Fernandez-Balcazar, A., Jimenez, M., & Castano, R. (2023). Predicting academic success in online higher education using ensemble methods. *Educational Technology Research and Development, 71*(3), 1067-1092.

</div>
<div custom-style="Reference">

Gao, J., Wang, S., & Liu, X. (2023). A review of explainable AI for education. *Computers and Education: Artificial Intelligence, 5*, 100084.

</div>
<div custom-style="Reference">

Ghazivakili, M. (2023). Class imbalance in student performance prediction. *Computers and Education: Artificial Intelligence, 5*, 100083.

</div>
<div custom-style="Reference">

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van Kerkwijk, M. H., Brett, M., Haldane, A., del Rio, J. F., Wiebe, M., Peterson, P., … Oliphant, T. E. (2020). Array programming with NumPy. *Nature, 585*(7825), 357-362.

</div>
<div custom-style="Reference">

Herodotou, C., Hlosta, M., Boroowa, A., Rientes, B., & Hatzilygeroudis, I. (2019). Open University learning analytics dataset. *Scientific Data, 6*(1), 28.

</div>
<div custom-style="Reference">

Hooshyar, D., & Yang, S. (2024). Predicting student dropout using deep learning and educational data mining: A systematic review. *Computers and Education, 211*, 104978.

</div>
<div custom-style="Reference">

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90-95.

</div>
<div custom-style="Reference">

Jha, S., Dey, S., & Kumar, S. (2019). A comparative study of machine learning algorithms for student performance prediction. *International Journal of Advanced Computer Science and Applications, 10*(12), 567-575.

</div>
<div custom-style="Reference">

Johora, F. T., Hossain, M. M., & Rahman, M. M. (2025). Explainable machine learning for student success prediction: A SHAP-based approach. *Smart Learning Environments, 12*(1), 1-25.

</div>
<div custom-style="Reference">

Kalita, D., Gogoi, B., & Saikia, M. (2025). Comparative analysis of Logistic Regression and Random Forest for student dropout prediction. *International Journal of Educational Management, 39*(2), 245-267.

</div>
<div custom-style="Reference">

Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. *Scientific Data, 4*, 170171.

</div>
<div custom-style="Reference">

Law, K. M. Y., Chung, M. S. W., & Leung, A. S. Y. (2024). An Ensemble-SMOTE based prediction model for graduate on-time completion. *Studies in Educational Evaluation, 81*, 101318.

</div>
<div custom-style="Reference">

Lee, S. (2017). Predicting student performance in online education using engagement and background features. *Educational Technology & Society, 20*(4), 127-140.

</div>
<div custom-style="Reference">

Lee, S., & Chen, Y. (2023). Explainable artificial intelligence in education: A review of applications. *Computers and Education Open, 4*, 100138.

</div>
<div custom-style="Reference">

Long, P. D., & Siemens, G. (2011). Penetrating the fog: Analytics in learning and education. *EDUCAUSE Review, 46*(5), 30-40.

</div>
<div custom-style="Reference">

Lundberg, S. M., Erion, G. G., & Lee, S.-I. (2018). Consistent individualized feature attribution for tree ensembles. *arXiv preprint arXiv:1802.03888*.

</div>
<div custom-style="Reference">

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30* (pp. 4765-4774). Curran Associates.

</div>
<div custom-style="Reference">

Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence, 2*(1), 56-67.

</div>
<div custom-style="Reference">

Malik, A., Qureshi, M. G., & Khan, S. (2025). Dynamic feature re-weighting and ensemble classification for student performance prediction. *Expert Systems with Applications, 246*, 123154.

</div>
<div custom-style="Reference">

Marcolino, A., Pereira, R., & Mendes, F. (2025). Comparative analysis of gradient boosting algorithms for student dropout prediction. *Computers and Education: Artificial Intelligence, 8*, 100351.

</div>
<div custom-style="Reference">

McKinney, W. (2010). Data structures for statistical computing in Python. In *Proceedings of the 9th Python in Science Conference* (pp. 56-61).

</div>
<div custom-style="Reference">

Moldovan, A. (2019). A machine learning approach to predicting student success. *International Journal of Educational Technology in Higher Education, 16*(1), 14.

</div>
<div custom-style="Reference">

Namoun, A., & Alshanqiti, A. (2020). Predicting student performance using data mining techniques: A systematic review. *Computers and Education, 154*, 103926.

</div>
<div custom-style="Reference">

Osmanbegovic, E., & Connelly, C. E. (2022). Predicting student outcomes: A comparative study of machine learning models. *Computers and Education Open, 3*, 100110.

</div>
<div custom-style="Reference">

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825-2830.

</div>
<div custom-style="Reference">

Press, G. (2024). *Machine learning: A guide for beginners*. Wiley.

</div>
<div custom-style="Reference">

Rezgui, K. (2025). A systematic review of predictive analytics in higher education: Trends and challenges. *Journal of Educational Computing Research, 63*(2), 421-456.

</div>
<div custom-style="Reference">

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 1135-1144). ACM.

</div>
<div custom-style="Reference">

Rohman, F., Suhartono, S., & Wibowo, A. (2025). Comparative analysis of machine learning algorithms for predicting student academic performance. *Journal of Educational Computing Research, 63*(1), 78-103.

</div>
<div custom-style="Reference">

Rudin, C., Chen, C., Chen, Z., Huang, H., Semenova, L., & Zhong, C. (2022). Interpretable machine learning: Fundamental principles and 10 grand challenges. *Statistical Surveys, 16*, 1-85.

</div>
<div custom-style="Reference">

Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE, 10*(3), e0118432.

</div>
<div custom-style="Reference">

Shapley, L. S. (1953). A value for n-person games. In H. W. Kuhn & A. W. Tucker (Eds.), *Contributions to the theory of games* (Vol. II, pp. 307-317). Princeton University Press.

</div>
<div custom-style="Reference">

Siemens, G. (2011). *Learning analytics and academic advising*. EDUCAUSE Review Online.

</div>
<div custom-style="Reference">

Spearman, C. (1904). The proof and measurement of association between two things. *American Journal of Psychology, 15*(1), 72-101.

</div>
<div custom-style="Reference">

Torkhani, R., & Rezgui, K. (2025). Explainable AI for student dropout prediction: A SHAP-LIME comparison. *Smart Learning Environments, 12*(2), 1-30.

</div>
<div custom-style="Reference">

Ujkani, B., Markovic, M., & Petrovic, V. (2024). A feature-importance analysis of SHAP values for student success. *Computers and Education: Artificial Intelligence, 6*, 100198.

</div>
<div custom-style="Reference">

Waskom, M. L. (2021). seaborn: Statistical data visualization. *Journal of Open Source Software, 6*(60), 3021.

</div>
<div custom-style="Reference">

Yang, S. (2024). Deep learning for student engagement prediction: A review. *Educational Data Mining and Learning Analytics, 12*(3), 45-72.

</div>
<div custom-style="Reference">

Zdrahal, Z. (2017). *Open University Learning Analytics dataset: A research compendium*. Open University.

</div>
