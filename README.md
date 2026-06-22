# health-insurance-claims-analyser
Exploratory data analysis + machine learning to identify what drives health insurance claim costs — with implications for Nigerian health finance and NHIA policy. 

---

## Problem

Nigeria's National Health Insurance Authority (NHIA) covers less than 5% of the population. A key barrier to scaling coverage is unsustainable claims expenditure: HMOs lose money on high-risk enrollees they cannot identify in advance, which suppresses willingness to expand coverage to informal sector workers and low-income households.

To design premiums that are both affordable and actuarially sound, you need to know: **what actually drives claim cost up and can predict it before someone enrolls?** 

Analysed 1,337 insurance claims across age, sex, BMI, smoking status, number of dependents, and region. Built two machine learning models: Linear Regression and Random Forest to identify cost drivers and predict individual claim amounts.

---

## Key findings

| Finding | What it means |
|--------|---------|
| **Smoking drives 3.8 times higher claims** | The single dominant cost variable: outweights age, BMI, refion, and sex combined |
| **BMI is the second predictor** | Chronic disease risk(diabetes, hypertension) are fast-growing cost burden in Nigeria |
| **55+ group costs 2.1 times more than under 25s** | Age-banded premium pricing is actuarially justified |
| **Region variation is minimal (~ $2,000 spread)** | Lifestyle factors outweight geography, location-based pricingg adds little value |
| **12.1% of claims exceed $30,000** | A small high-cost minority drives disproportionate financial exposure across the pool |

---
## Recommendation

1. **Weight smoking status heavily** In any Nigerian HMO premium model: it is the strongest predictor by a significant margin.
2. **Introduce BMI-based risk screening** at enrollment: Early identification of chronic disease risk reduces long-term claims
3. **Design age-banded premium tiers**: The cost escalation from young to older enrolles is consistent and predictable.
4. **Invest in smoker wellness programmes**: The cost differential is large enough that even modest quit rates would materially reduce claims expenditure.

## Impact (next version)

Apply this same framework to real Nigerian NHIA claims with LGA geography, ICD-10 diagnosis codes, and facility type. The result is an actionable underwriting tool that helps Nigerian HMOs price risk sustainably and helps NHIA model the actuarial cost of universal coverage expansion.

## Machine learning results

| Metric | Linear Regression | Random Forest |
|--------|:-----------------:|:-------------:|
| R² (variance explained) | 80.7% | **88.3%** |
| MAE (avg prediction error) | $4,182 | **$2,556** |
| RMSE | $5,958 | **$4,628** |

**Random Forest** expains 88% of why claim costs differ between patients, sufficient accuracy for exploratory premuim modelling and risk segmentation.

---

## Feature importance: What actually drives costs

| Feature | Importance | Interpretation |
|---------|:-----------| :--------------|
| Smoking status | 0.60 | Dominant variable: 3.8x cost multiplier |
| BMI | 0.21 | Chronic disease proxy |
| Age | 0.14 | Consistent escalation across groups |
| Children | 0.03 | Minimal impact |
| Region | 0.02 | Geography barely matters |
| Sex | 0.01 | Negligible cost difference

## Project structure

```
health-insurance-claims-analyser/
│
├── ml_model.ipynb          # Full ML notebook — EDA + Linear Regression + Random Forest
├── dashboard.py            # Interactive Streamlit dashboard
├── medical_cost.csv        # Dataset (US Medical Insurance Costs)
├── requirements.txt        # Python dependencies
│
├── chart1_cost_distribution.png
├── chart2_age_group_costs.png
├── chart3_smoker_cost.png
├── chart4_feature_importance.png
└── chart5_actual_vs_predicted.png
```

---

## How to run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Jupyter notebook (ML model + EDA)
```bash
jupyter notebook ml_model.ipynb
```
Or open directly in VS Code — select the `.ipynb` file and run cells with **Shift + Enter**.

### Run the interactive dashboard
```bash
streamlit run dashboard.py
```
Opens at `http://localhost:8501` — use sidebar filters to explore cost patterns interactively.

---

## Charts produced

**Chart 1 — Cost distribution**  
Right-skewed: bulk of claims under $15,000 but a long tail to $63,770 signals a high-risk subgroup.

**Chart 2 — Cost by age group**  
Consistent escalation from under-25 (~$9,000 avg) to 55+ (~$19,000 avg).

**Chart 3 — Smoker vs non-smoker**  
The starkest finding: a nearly 4x cost gap that holds across all demographics.

**Chart 4 — Feature importance**  
Smoking (0.60) → BMI (0.21) → Age (0.14) → Children, Region, Sex (minimal).

**Chart 5 — Actual vs predicted**  
Random Forest predictions cluster tightly around the perfect-prediction line vs Linear Regression scatter.

---

## Dataset & Nigerian context

This project uses US Medical insurance costs data as a proof-of-concept: 1,338 records (public domain). The same analytical framework applied to Nigerian NHIS/NHIA claims data would need:

- **Replace region** with State / LGA-level geography
- **Add ICD-10 diagnosis codes** for disease-specific cost analysis
- **Add facility type** (primary/secondary/tertiary) as a cost predictor
- **Add NHIA enrollment status** to model uptake vs non-enrollment patterns

The result would be an actionable underwriting and policy planning tool for Nigerian HMOs and state health schemes.

---

*Build as part of a structured health finance data science portfolio at the Digital Healthcare Interoperability Network (DHIN), Abuja, Nigeria.*
