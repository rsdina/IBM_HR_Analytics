# IBM HR Analytics

Interactive employee attrition intelligence dashboard built with Streamlit.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens with a dark neon visual system inspired by the project reference: magenta, cyan, orange, and lime accents over an editorial purple-black canvas.

## Dashboard views

- **Overview:** workforce KPIs, attrition mix, department signal, and action-oriented insights.
- **Drivers:** model coefficients, tenure patterns, and job-role attrition.
- **Model lab:** exported model comparison and validation metrics.
- **Employee explorer:** searchable, filter-aware employee table with CSV download.
- **Risk simulator:** interactive what-if prediction using the exported Logistic Regression model and scaler.

## Project artifacts

The app reads the existing files under `data/`, `models/`, and `reports/`. The risk simulator follows the notebook's original preprocessing contract: alphabetical label encoding for categorical fields, removal of identifier/constant columns, and use of the saved `StandardScaler` before prediction.
