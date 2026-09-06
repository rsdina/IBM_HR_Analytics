# IBM HR Analytics

An end-to-end employee attrition analytics project based on the IBM HR Analytics dataset. The repository includes the analysis notebook, cleaned data, trained models, static charts, generated reports, and a permanent Streamlit dashboard for exploring the results.

## Live dashboard experience

The Streamlit app is the primary interface for this project. It uses a dark editorial canvas with magenta, cyan, orange, and lime accents to make workforce signals easy to scan without hiding the underlying detail.

The dashboard includes:

- **Overview:** filtered workforce KPIs, attrition mix, department signal, compensation gap, and retention insights.
- **Drivers:** Logistic Regression coefficients, tenure patterns, and job-role attrition rates.
- **Model lab:** Accuracy, precision, recall, F1, and AUC-ROC comparisons for every exported model.
- **Employee explorer:** Searchable employee records with CSV export for the active filter slice.
- **Risk simulator:** What-if employee scenarios scored by the saved Logistic Regression model.

## Run the dashboard locally

From the repository root:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS or Linux
source .venv/bin/activate
```

Install the application dependencies and start Streamlit:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the URL shown by Streamlit, normally `http://localhost:8501`.

## Live Streamlit App
https://ibmhranalytics-cchappgmjcyu5xnimxyvs4p.streamlit.app/


The app is self-contained: it loads data and model artifacts with paths relative to `app.py`, so the `data/` and `models/` folders must remain in the repository.

## Repository layout

```text
IBM_HR_Analytics/
├── app.py                         # Streamlit dashboard entry point
├── HR_Analytics.ipynb             # Analysis, preprocessing, and training workflow
├── requirements.txt               # Dashboard and model runtime dependencies
├── charts/                        # Exported analysis charts
├── data/
│   ├── cleaned_hr_dataset.csv     # 1,470 employee records and target labels
│   ├── feature_importance.csv     # Logistic Regression coefficients
│   └── model_performance.csv      # Model comparison metrics
├── models/
│   ├── best_model.pkl              # Saved Logistic Regression model
│   ├── scaler.pkl                  # Saved StandardScaler
│   ├── feature_columns.json        # Inference feature order
│   └── model_metadata.json         # Training and validation metadata
└── reports/
	├── summary_report.md           # Human-readable findings
	└── summary_report.html         # Browser-ready report
```

## Project results

The exported analysis contains 1,470 employees and reports:

- **16.12%** overall attrition rate, representing 237 employees.
- **Sales** as the highest-attrition department at 20.63%.
- A monthly income gap of approximately **$2,046** between employees who stayed and employees who left.
- **Logistic Regression** as the best exported model by accuracy, with 87.41% accuracy and 0.806 AUC-ROC.
- **OverTime** as the strongest positive attrition driver in the saved coefficient ranking.

## Model inference

The simulator follows the original notebook's preprocessing contract:

1. Categorical columns are label-encoded alphabetically, matching `LabelEncoder` behavior used during training.
2. Identifier and constant columns are removed.
3. Numeric defaults use dataset medians and categorical defaults use dataset modes.
4. The resulting 30 features are transformed with the saved `StandardScaler`.
5. The saved Logistic Regression model returns an attrition probability.

The risk score is a prioritization signal for workforce analysis, not a standalone employment decision. Validate any model signal with context, human review, and fair HR practices.

## Reproduce the analysis

Open `HR_Analytics.ipynb` in Jupyter or Google Colab to review the original data cleaning, exploratory analysis, model training, evaluation, and export workflow. The dashboard consumes the exported artifacts already committed under `data/`, `models/`, `charts/`, and `reports/`.
