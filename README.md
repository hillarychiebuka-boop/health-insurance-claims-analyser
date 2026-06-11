# health-insurance-claims-analyser
Exploratory data analysis + machine learning to identify what drives health insurance claim costs — with implications for Nigerian health finance and NHIA policy.

**Author:** Hillary Onah — Finance & Data Science Analyst, DHIN  
**Built:** June 2026 | **Stack:** Python · Pandas · Scikit-learn · Streamlit · Plotly  

---

## Project overview

Nigeria's National Health Insurance Authority (NHIA) covers less than 5% of the population. A key barrier to scaling coverage is the inability to accurately price risk and predict claim costs across different enrollee profiles.

This project analyses health insurance claims data to answer three practical questions:

1. **What is the distribution of claim costs** — and where does financial risk concentrate?
2. **Which patient characteristics drive costs up** — age, lifestyle, geography, or demographics?
3. **Can we predict a patient's likely claim cost** from their profile with reasonable accuracy?

The answers have direct applications for HMO premium design, NHIA actuarial modelling, and state-level Contributory Health Scheme planning.

---

## Key findings

| Finding | Insight |
|--------|---------|
| **Smoking is the #1 cost driver** | Smokers generate claims **3.8x higher** than non-smokers — importance score 0.60 in Random Forest model |
| **BMI is the second predictor** | Relevant for chronic disease profiling — diabetes and hypertension are fast-growing cost drivers in Nigeria |
| **Age escalates costs consistently** | 55+ group costs **2.1x more** than under-25s — age-banded pricing is actuarially justified |
| **Region barely matters** | Only ~$2,000 spread across regions — lifestyle factors outweigh geography |
| **Cost distribution is right-skewed** | Most claims are low-cost, but a high-cost tail (>$30k) drives disproportionate financial exposure |

---

## Machine learning results

| Metric | Linear Regression | Random Forest |
|--------|:-----------------:|:-------------:|
| R² (variance explained) | 80.7% | **88.3%** |
| MAE (avg prediction error) | $4,182 | **$2,556** |
| RMSE | $5,958 | **$4,628** |

**Random Forest wins** — complex interactions between risk factors exist that a linear model cannot capture. The 88.3% R² means the model explains the vast majority of why claim costs differ between patients.

---

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

## Tech stack

| Tool | Purpose |
|------|---------|
| `pandas` | Data loading, cleaning, transformation |
| `matplotlib` / `seaborn` | Static charts |
| `plotly` | Interactive dashboard charts |
| `scikit-learn` | Linear Regression + Random Forest models |
| `streamlit` | Interactive web dashboard |

---

## Nigerian context & next steps

This project uses US insurance data as a proof-of-concept. The same analytical framework applied to Nigerian NHIS/NHIA claims data would need:

- **Replace region** with State / LGA-level geography
- **Add ICD-10 diagnosis codes** for disease-specific cost analysis
- **Add facility type** (primary/secondary/tertiary) as a cost predictor
- **Add NHIA enrollment status** to model uptake vs non-enrollment patterns

The result would be an actionable underwriting and policy planning tool for Nigerian HMOs and state health schemes.

---

##  Related projects (coming soon)

- Out-of-pocket health spending vs income — Nigerian households
- Hospital revenue leakage detector
- Nigeria health financing gap dashboard

---

*Starter portfolio project built as part of a structured health finance data science learning journey*
